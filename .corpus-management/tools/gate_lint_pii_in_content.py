#!/usr/bin/env python3
"""PII-content audit (grc gate): pack-owned engine (source of record).

Scan content for suspected personally-identifying information: email addresses
(excluding an allow-list of documentation / example / maintainer-contact
domains supplied by the caller), US SSN patterns, US phone numbers, public IPv4
addresses (documentation / private / reserved / version-number-shaped matches
are filtered out), and postal street-address fragments. Lines inside fenced code
blocks are skipped (the shared fence-aware scan).

Engine/wrapper split (SHARED/SAFETY lane PR-38, Pattern A): this engine carries the
detection regexes (``EMAIL_RE``, ``US_SSN_RE``, ``US_PHONE_RE``, ``IPV4_RE``,
``STREET_RE``), the IP filters (``is_documentation_ip``, ``is_version_ip``), and the
pure ``scan``; the project wrapper (``tools/lint-pii-in-content.py``) supplies the grc
scan scope (the scanned-suffix set and the exempt-file set, which includes THIS engine
because it documents the PII formats by design) and the grc example-domain allow-list,
and keeps a thin module-global ``scan`` shim delegating here so the scan-scope
regression test (which patches ``mod.scan`` and runs ``main``) observes the original
signature and behaviour. ``scan`` takes ``example_domains`` as a keyword so the engine
carries no grc-specific allow-list; the wrapper supplies it. The engine is scope-free
and repository-root-free.

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
        "gate_lint_pii_in_content: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


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
        # (e.g., guardrails/core/owasp.md) must be able to
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


def scan(path: Path, *, example_domains) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        # Email addresses
        for m in EMAIL_RE.finditer(line):
            local, domain = m.group(1), m.group(2).lower()
            if domain in example_domains:
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
