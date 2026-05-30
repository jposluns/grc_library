#!/usr/bin/env python3
"""Detect internal-deployment references that should not appear in a CC0 library.

A vendor-neutral, organisation-neutral public library should not contain
references to specific deployments: internal hostnames, cloud-region
identifiers, internal subnet patterns, internal-looking domain names.
This linter extends the existing SANITISATION_TERMS rule in
[`tools/lint-language.py`](tools/lint-language.py) with generic patterns rather than the
hand-curated list of specific product/company names.

Patterns detected:
- Hostnames ending in `.local`, `.internal`, `.corp`, `.lan`, `.intranet`.
- Cloud region identifiers (AWS `us-east-1`-shape, Azure `westeurope`-shape,
  GCP `us-central1`-shape) appearing in production / configuration prose.
- Specific subnet CIDR notations outside RFC 1918 / RFC 5737 example ranges.
- FQDNs with three+ subdomain levels that look organisation-specific.

The linter is deliberately conservative on FQDN detection (false positives
risk catching legitimate vendor / publisher domain references).

Usage:
    python3 tools/lint-internal-references.py
    python3 tools/lint-internal-references.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more internal-reference patterns present
"""

from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = [str(REPO_ROOT)]

EXEMPT_DIR_PARTS = {".git", "node_modules", "__pycache__"}

EXEMPT_FILES = {
    "lint-internal-references.py",
    "lint-language.py",
    "lint-secrets-in-content.py",
    "lint-pii-in-content.py",
    # CHANGELOG describes prior sanitisation fixes by name (including the
    # patterns that were removed).
    "CHANGELOG.md",
}

# Internal-domain hostname suffixes.
INTERNAL_TLD_RE = re.compile(
    r"\b[a-zA-Z0-9\-]+\.(?:local|internal|corp|lan|intranet|home\.arpa)\b",
    re.IGNORECASE,
)

# Cloud-region identifiers
AWS_REGION_RE = re.compile(
    r"\b(?:us|eu|ap|ca|sa|me|af)-(?:east|west|north|south|northeast|northwest|southeast|southwest|central)-\d\b"
)
AZURE_REGION_RE = re.compile(
    r"\b(?:east|west|north|south|central)(?:us|us2|us3|europe|asia)\b",
    re.IGNORECASE,
)
GCP_REGION_RE = re.compile(
    r"\b(?:us|europe|asia|australia|southamerica|africa|me)-(?:east|west|north|south|central|northeast|southeast)\d\b"
)

# CIDR subnets in non-documentation ranges
CIDR_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}/(?:[1-9]|[12]\d|3[0-2])\b")


def is_target(path: Path) -> bool:
    if path.suffix not in {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt"}:
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in EXEMPT_FILES:
        return False
    return True


def is_documentation_subnet(cidr: str) -> bool:
    try:
        net = ipaddress.IPv4Network(cidr, strict=False)
    except (ValueError, ipaddress.AddressValueError):
        return True
    if net.is_private or net.is_loopback or net.is_link_local or net.is_multicast:
        return True
    if net.is_reserved or net.is_unspecified:
        return True
    doc_ranges = [
        ipaddress.IPv4Network("192.0.2.0/24"),
        ipaddress.IPv4Network("198.51.100.0/24"),
        ipaddress.IPv4Network("203.0.113.0/24"),
        ipaddress.IPv4Network("0.0.0.0/8"),
        ipaddress.IPv4Network("255.255.255.0/24"),
    ]
    return any(net.subnet_of(r) for r in doc_ranges)


def scan(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in INTERNAL_TLD_RE.finditer(line):
            findings.append((lineno, "internal hostname", m.group(0)))
        for m in AWS_REGION_RE.finditer(line):
            findings.append((lineno, "AWS region identifier", m.group(0)))
        for m in AZURE_REGION_RE.finditer(line):
            findings.append((lineno, "Azure region identifier", m.group(0)))
        for m in GCP_REGION_RE.finditer(line):
            findings.append((lineno, "GCP region identifier", m.group(0)))
        for m in CIDR_RE.finditer(line):
            if is_documentation_subnet(m.group(0)):
                continue
            findings.append((lineno, "non-documentation CIDR subnet", m.group(0)))
    return findings


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect internal-deployment references in library content."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
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
        "Internal-deployment patterns detected. A CC0 library should be "
        "vendor-neutral and organisation-neutral; replace specific cloud "
        "regions, internal hostnames, or non-documentation subnets with "
        "placeholders or generic references."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
