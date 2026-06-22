#!/usr/bin/env python3
"""Detect personal identifiable information (PII) patterns in library content.

The library is meant to be organisation-neutral and individual-neutral.
Personal data in CC0-published content is a privacy issue: anyone
adopting the library inherits whatever names, emails, phone numbers,
or addresses appear in the source. This linter defends against
sanitisation gaps.

Patterns detected:
- Email addresses (other than maintainer contact files and example
  domains).
- US Social Security Number patterns (3-2-4 digit form).
- US phone numbers (10-digit forms with separators).
- Plausible postal-address fragments (street number + street name).
- IPv4 addresses outside RFC 1918 / documentation ranges (10/8,
  172.16/12, 192.168/16, 127/8, 169.254/16, 192.0.2/24, 198.51.100/24,
  203.0.113/24).

The linter is deliberately conservative on email and addresses to
avoid false positives on documentation examples.

Exemption layers:

  - EXAMPLE_DOMAINS: emails on ``example.com``, ``example.org``,
    ``example.net``, and ``posluns.ca`` (the maintainer's contact
    address, kept available for adopter contact) are not flagged.
  - Version-string heuristic: IPv4-shaped strings that look like
    software versions (e.g., ``4.0.1.2`` adjacent to "v" or "version"
    or "Rev") are treated as version numbers, not addresses.
  - Per-file exemptions: a small set of AI security guides and
    research notes whose content legitimately includes IP-shaped
    threat indicators or address examples.
  - CHANGELOG.md is exempt because it can describe sanitisation fixes
    that quote (now-removed) PII.
  - Fenced code blocks are skipped so example syntax does not produce
    false positives.

Usage:
    python3 tools/lint-pii-in-content.py
    python3 tools/lint-pii-in-content.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more suspected PII patterns present
"""

from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, iter_targets, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

SCAN_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt", ".cff"}

# Files exempt because they intentionally contain maintainer contact info
# (CITATION.cff and AUTHORS.md) or describe PII patterns by example
# (privacy standards, the PII linter source itself).
EXEMPT_FILES = {
    "AUTHORS.md",
    "CITATION.cff",
    "lint-pii-in-content.py",
    "lint-language.py",  # contains sanitization-term list
    "lint-secrets-in-content.py",  # discusses secret/PII patterns
    "lint-internal-references.py",  # discusses IP / hostname patterns
    # Linter regression tests deliberately embed PII-shaped strings as
    # test inputs.
    "test_linters.py",
    # The adversarial test reference contains documentation of attack
    # patterns including fake emails used as prompt-injection test inputs.
    # The emails are intentional test data, not real PII.
    "guide-ai-adversarial-test-reference.md",
    # AI security technical implementation guide contains test/example emails.
    "guide-ai-security-technical-implementation.md",
    # CHANGELOG describes linter patterns including test cases (e.g., CIDR
    # examples) that incidentally match PII patterns.
    "CHANGELOG.md",
}

# Domains acceptable in documentation examples. An email on one of
# these domains is not flagged as suspected PII because the domain
# itself signals an example / placeholder / RFC-reserved context.
#
# Note: the template-placeholder domains (yourcompany.com,
# your-org.com, your-org.example.com) are kept here because in a
# template they are legitimate non-PII fill-in markers. They are
# additionally registered as patterns in lint-placeholder-leakage.py
# (Phase 23.63), so leaving one in production content is flagged
# defensively by that linter while still avoiding a false-positive
# PII finding here.
EXAMPLE_DOMAINS = {
    # RFC 2606 reserved example domains
    "example.com", "example.org", "example.net",
    "test", "localhost", "invalid",
    # Template-placeholder organisation domains (see note above)
    "yourcompany.com", "your-org.com", "your-org.example.com",
    # Generic third-party stand-ins used in worked examples
    "competitor.com", "attacker.com", "evil.com",
    # RFC-reserved .example TLD used in security-awareness examples
    "phishing.example", "malicious.example",
    # The library maintainer's contact domain (recorded in AUTHORS / CITATION):
    "posluns.ca",
}
# Phase 23.63 removed `noreply.github.com` (no corpus reference)
# and `posluns.com` (only `.ca` is used in AUTHORS / CITATION).

EMAIL_RE = re.compile(r"\b([a-zA-Z0-9._%+\-]+)@([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})\b")
US_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
# Strict US phone: optional +1, then 3-3-4 with separators.
US_PHONE_RE = re.compile(r"\b(?:\+1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b")
# IPv4 must be exactly 4 dotted octets, not part of a longer dotted
# sequence (which would be an OID like 1.3.6.1.5.5.7.3 or similar).
IPV4_RE = re.compile(r"(?<![.\d])(?:\d{1,3}\.){3}\d{1,3}(?![.\d])")
# Plausible US street-number-then-name. Conservative: require number + 2+ words + suffix.
STREET_RE = re.compile(
    r"\b\d{1,5}\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+"
    r"(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Boulevard|Blvd\.?|Lane|Ln\.?|Drive|Dr\.?|Court|Ct\.?|Way|Place|Pl\.?)"
    r"\b"
)


def is_documentation_ip(addr: str) -> bool:
    """Return True if the IP is in a documentation/private range."""
    try:
        ip = ipaddress.IPv4Address(addr)
    except (ValueError, ipaddress.AddressValueError):
        return True  # not a valid IP; treat as not-real
    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
        return True
    if ip.is_reserved or ip.is_unspecified:
        return True
    # IETF documentation ranges (RFC 5737)
    doc_ranges = [
        ipaddress.IPv4Network("192.0.2.0/24"),
        ipaddress.IPv4Network("198.51.100.0/24"),
        ipaddress.IPv4Network("203.0.113.0/24"),
        # Common documentation example ranges
        ipaddress.IPv4Network("0.0.0.0/8"),
        ipaddress.IPv4Network("255.255.255.0/24"),
        # CGNAT shared address space (RFC 6598). Python's
        # IPv4Address.is_private returns True for this range only on
        # Python 3.13+; this explicit network keeps recognition
        # backward-compatible. Documentation citing the SSRF block-list
        # (e.g., dev-security/claude-rules/core/owasp.md) must be able to
        # quote the range without triggering this gate.
        ipaddress.IPv4Network("100.64.0.0/10"),
    ]
    return any(ip in r for r in doc_ranges)


def is_version_ip(line: str, start: int) -> bool:
    """Heuristic: is the IP-shaped match actually a version number?

    Version numbers like "4.0.1.2" can match the IPv4 regex. If the
    surrounding context contains "version", "v" prefix, or "release",
    treat as version not IP.
    """
    window = line[max(0, start - 30):start + 30].lower()
    indicators = ("version", "release", "rev ", "v1.", "v2.", "v3.", "v4.", "v5.")
    return any(ind in window for ind in indicators)


def scan(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        # Email addresses
        for m in EMAIL_RE.finditer(line):
            local, domain = m.group(1), m.group(2).lower()
            if domain in EXAMPLE_DOMAINS:
                continue
            # Skip obvious GitHub username @ patterns ("@user" not "user@domain")
            findings.append((lineno, "email address", m.group(0)))
        # SSN
        for m in US_SSN_RE.finditer(line):
            findings.append((lineno, "US SSN pattern", m.group(0)))
        # Phone
        for m in US_PHONE_RE.finditer(line):
            findings.append((lineno, "US phone number", m.group(0)))
        # IPv4 (filter for non-documentation only)
        for m in IPV4_RE.finditer(line):
            addr = m.group(0)
            if is_documentation_ip(addr):
                continue
            if is_version_ip(line, m.start()):
                continue
            findings.append((lineno, "public IPv4 address", addr))
        # Street addresses
        for m in STREET_RE.finditer(line):
            findings.append((lineno, "postal address fragment", m.group(0)))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect PII patterns in library content."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(
        args.paths,
        suffixes=SCAN_SUFFIXES,
        exempt_files=EXEMPT_FILES,
    )
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: no suspected PII patterns (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, label, value in findings:
            print(f"  L{lineno} [pii-pattern] {label}: {value}")
        total += len(findings)
    print(f"\nFAIL: {total} suspected PII finding(s) across {len(grouped)} file(s).")
    print(
        "Personal data patterns detected in library content. Library is "
        "CC0 and meant to be individual-neutral; replace any real PII with "
        "documentation-example placeholders or move maintainer contact to "
        "AUTHORS.md / CITATION.cff."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
