#!/usr/bin/env python3
"""Detect internal-deployment references that should not appear in an openly-published (CC BY-SA 4.0) library.

A vendor-neutral, organization-neutral public library should not contain
references to specific deployments: internal hostnames, cloud-region
identifiers, internal subnet patterns. This linter detects them structurally, with generic regex patterns
rather than a hand-curated list of specific product or company names.

Patterns detected:

  - Hostnames ending in `.local`, `.internal`, `.corp`, `.lan`,
    `.intranet`, `home.arpa` (INTERNAL_TLD_RE).
  - Cloud-region identifiers (AWS `us-east-1`-shape, Azure
    `westeurope`-shape, GCP `us-central1`-shape) appearing in
    production / configuration prose (per-provider region regexes).
  - Specific subnet CIDR notations outside RFC 1918 (private) /
    RFC 5737 (documentation) ranges, plus loopback, link-local,
    multicast, reserved, unspecified, 0.0.0.0/8, 255.255.255.0/24, and
    CGNAT 100.64.0.0/10 (CIDR_RE); an unparseable CIDR is treated as
    documentation (fail-open).

The linter is deliberately conservative. FQDN-shape detection is NOT
implemented; the false-positive risk on legitimate vendor / publisher
domain references is too high. Identifying organization-specific FQDNs
requires either an allow-list or a deny-list, neither of which has been
curated for the corpus.

Usage:
    python3 tools/lint-internal-references.py
    python3 tools/lint-internal-references.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more internal-reference patterns present
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import REPO_ROOT, iter_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

SCAN_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt"}

EXEMPT_FILES = {
    "lint-internal-references.py",
    "lint-language.py",
    "lint-secrets-in-content.py",
    "lint-pii-in-content.py",
    # CHANGELOG describes prior sanitization fixes by name (including the
    # patterns that were removed).
    "CHANGELOG.md",
    # Linter regression tests deliberately embed internal-host-shaped
    # strings as test inputs.
    "test_linters.py",
    # The pack-owned engine (gate_lint_internal_references.py) now holds the
    # detection regexes, so it documents the internal-reference formats by design
    # exactly as this wrapper did before the PR-39 transfer; exempt it likewise.
    "gate_lint_internal_references.py",
}


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_internal_references  # the pack-owned engine (source of record)
    return gate_lint_internal_references


def scan(path: Path) -> list[tuple[int, str, str]]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression
    test patches ``mod.scan`` and runs ``main``; the detection regexes and the
    check live in the pack engine (gate_lint_internal_references.py).
    """
    return _engine().scan(path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect internal-deployment references in library content."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(
        args.paths,
        suffixes=SCAN_SUFFIXES,
        exclude_default_roots=False,  # Preserve source-tree safety coverage.
        exempt_files=EXEMPT_FILES,
    )
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: no internal-reference patterns (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, label, value in findings:
            print(f"  L{lineno} [internal-reference] {label}: {value}")
        total += len(findings)
    print(f"\nFAIL: {total} internal-reference finding(s) across {len(grouped)} file(s).")
    print(
        "Internal-deployment patterns detected. An openly-published (CC BY-SA 4.0) library should be "
        "vendor-neutral and organization-neutral; replace specific cloud "
        "regions, internal hostnames, or non-documentation subnets with "
        "placeholders or generic references."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
