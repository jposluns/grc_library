#!/usr/bin/env python3
"""CCM family-range provider-to-tenant member direction - grc wrapper over the pack engine.

Flag a CCM family-range citation (e.g. "CCC-01 to 09") that sweeps in a
provider-to-tenant ("directional") control member on an internal-scope document.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(RANGE_RE, swept_members, the fence/inline-code regexes, scan_text) is the source
of record in the pack engine
(.corpus-management/tools/gate_lint_ccm_provider_member_in_range.py); it carries no
project catalogue and takes the directional-member set via configure(). This wrapper
supplies DIRECTIONAL_PROVIDER_MEMBERS, configures the engine, and keeps the scan
scope (scan_targets), a module-global scan_text shim, main, and the exit codes.
"""

from __future__ import annotations

import sys
from pathlib import Path

from lint_common import (  # noqa: E402  # grc-config/store, stays local
    DEFAULT_EXEMPT_DIRS,
    REPO_ROOT,
    iter_markdown_targets,
    read_text_safe,
)

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"


DIRECTIONAL_PROVIDER_MEMBERS: frozenset[str] = frozenset(
    {"I&S-06", "CCC-05", "LOG-08", "STA-04", "DSP-18", "CEK-08", "IAM-11", "IPY-02"}
)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_ccm_provider_member_in_range  # the pack-owned engine (source of record)
    return gate_lint_ccm_provider_member_in_range


# Configure the engine ONCE with the grc directional-member set.
_engine().configure(DIRECTIONAL_PROVIDER_MEMBERS)


def scan_text(rel: str, text: str) -> list:
    """Thin shim delegating to the pack engine's pure scan (engine already configured)."""
    return _engine().scan_text(rel, text)


def scan_targets(roots: list[Path] | None = None) -> list[Path]:
    """The gate's file-discovery scope: corpus Markdown, exempting the shared
    exempt dirs plus the ``guardrails/`` pack and ``CHANGELOG.md``. Exposed as a
    module function so the scan-scope regression can model the real scope."""
    root = Path(REPO_ROOT)
    scan_roots = roots or [root]
    return list(
        iter_markdown_targets(
            scan_roots,
            exempt_dirs=frozenset(DEFAULT_EXEMPT_DIRS) | {"guardrails"},
            exempt_files=("CHANGELOG.md",),
        )
    )


def main(argv: list[str]) -> int:
    root = Path(REPO_ROOT)
    scan_roots = [Path(p).resolve() for p in argv[1:]] or [root]
    all_findings: list[str] = []
    try:
        for path in scan_targets(scan_roots):
            text = read_text_safe(path)
            if text is None:
                continue
            rel = str(path.relative_to(root))
            all_findings.extend(scan_text(rel, text))
    except Exception as exc:  # top-level guard: any internal error -> exit 2 (the contract)
        print(f"ERROR: internal error during CCM range-direction scan: {exc}", file=sys.stderr)
        return 2
    if all_findings:
        print(
            "FAIL: CCM family-range citation(s) sweep in a provider-to-tenant "
            "member on an internal-scope document:",
            file=sys.stderr,
        )
        for f in all_findings:
            print(f"  {f}", file=sys.stderr)
        return 1
    print(
        "OK: no CCM family-range citation sweeps in any of the "
        f"{len(DIRECTIONAL_PROVIDER_MEMBERS)} tracked provider-to-tenant control members "
        "on an internal-scope document (checked by range-membership, not token grep; "
        "the tracked set is the known directional members and is extended as new ones surface)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
