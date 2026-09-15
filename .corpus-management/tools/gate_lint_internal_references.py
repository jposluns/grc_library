#!/usr/bin/env python3
"""Internal-reference audit (grc gate): pack-owned engine (source of record).

Scan content for internal-deployment references that an openly-published,
organization-neutral corpus should not carry: internal-domain hostnames
(``.local`` / ``.internal`` / ``.corp`` / ``.lan`` / ``.intranet`` / ``home.arpa``,
excluding filenames with those stems), cloud-region identifiers (AWS / Azure / GCP),
and CIDR subnets outside the documentation / private / reserved ranges. Lines inside
fenced code blocks are skipped (the shared fence-aware scan).

Engine/wrapper split (SHARED/SAFETY lane PR-39, Pattern A): this engine carries the
detection regexes (``INTERNAL_TLD_RE``, ``AWS_REGION_RE``, ``AZURE_REGION_RE``,
``GCP_REGION_RE``, ``CIDR_RE``), the subnet filter (``is_documentation_subnet``), and
the pure ``scan``; the project wrapper (``tools/lint-internal-references.py``) supplies
the grc scan scope (the scanned-suffix set and the exempt-file set, which includes THIS
engine because it documents the internal-reference formats by design) and the grouped
reporting in ``main``, and keeps a thin module-global ``scan`` shim delegating here so
the scan-scope regression test (which patches ``mod.scan`` and runs ``main``) observes
the original signature and behaviour. The engine's ``scan`` is scope-free and
repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import ipaddress
import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_internal_references: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


# Internal-domain hostname suffixes. The trailing negative lookahead excludes
# FILENAMES whose stem ends in one of these words followed by a file extension
# (e.g. the Claude Code machine-local settings file `settings.local.json`): a
# `.local`/`.internal`/etc. immediately followed by a `.<ext>` is a file, not an
# internal hostname. It does not exclude subdomain chains (a `.corp.example.com`
# is followed by `.example`, not a listed extension), so genuine internal FQDNs
# stay flagged.
INTERNAL_TLD_RE = re.compile(
    r"\b[a-zA-Z0-9\-]+\.(?:local|internal|corp|lan|intranet|home\.arpa)\b"
    r"(?!\.(?:json|ya?ml|toml|md|txt|lock|cfg|ini|conf|py|js|ts|sh))",
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
        # CGNAT shared address space (RFC 6598). Python's
        # IPv4Network.is_private returns True for this range only on
        # Python 3.13+; this explicit network keeps recognition
        # backward-compatible.
        ipaddress.IPv4Network("100.64.0.0/10"),
    ]
    return any(net.subnet_of(r) for r in doc_ranges)


def scan(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
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
