#!/usr/bin/env python3
"""PII-content audit (grc gate): pack-owned engine (source of record).

Scan content for suspected personally-identifying information: email addresses
(excluding a caller-supplied allow-list of documentation / example /
maintainer-contact domains, plus the RFC 2606 / RFC 6761 reserved TLDs
.invalid/.test/.example/.localhost), US SSN patterns, US phone numbers, public IPv4
addresses (documentation / private / reserved / version-number-shaped matches
are filtered out, as are four-part standard clause numbers cited after a section
sign, "section(s)", "clause(s)" or a standard designator, or later in a list of
four-part clause numbers one of these opens; a match with a port, a CIDR suffix or a
URL scheme in the same token is never treated as a citation), and postal
street-address fragments.
Lines inside fenced code blocks are skipped (the shared fence-aware scan).

Engine/wrapper split (SHARED/SAFETY lane PR-38, Pattern A): this engine carries the
detection regexes (``EMAIL_RE``, ``US_SSN_RE``, ``US_PHONE_RE``, ``IPV4_RE``,
``STREET_RE``), the IP filters (``is_documentation_ip``, ``is_version_ip``, ``is_citation_ip``),
and the pure ``scan``; the project wrapper (``tools/lint-pii-in-content.py``) supplies the grc
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
import unicodedata
from pathlib import Path

try:
    import idna  # exact UTS-46 domain-label validity for the email/domain boundary test
    _HAVE_IDNA = True
except ImportError:  # bare adopter clone without idna: degrade to the FN-safe approximation below
    _HAVE_IDNA = False

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_pii_in_content: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


EMAIL_RE = re.compile(r"\b([a-zA-Z0-9._%+\-]+)@([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})\b")
# RFC 2606 s.2 / RFC 6761 reserved TLDs: not publicly registrable, so an email on
# one is a placeholder/example address rather than a real public mailbox. This is
# an example-domain policy signal, not proof of non-identifiability: RFC 6761 still
# permits private .test resolution and .localhost loopback, so a private-network
# deployment could resolve one. Matched as a suffix (the leading dot enforces a
# label boundary) rather than an exact host, unlike the caller-supplied
# EXAMPLE_DOMAINS allowlist. Do not fold these into EXAMPLE_DOMAINS: that set is
# exact-match by design and folding would broaden project-specific exemptions.
RESERVED_EMAIL_SUFFIXES = (".invalid", ".test", ".example", ".localhost")
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
# Citation context for an IPv4-shaped match (``is_citation_ip``). A four-part
# standard clause number ("section 8.2.2.1", "IEEE 2883-2022 clauses 8.3.1.1,
# 8.3.1.2 and 8.3.1.3") matches IPV4_RE. The text before such a match ends with a
# cue (a section sign; "section", "sections", "clause" or "clauses" in any letter
# case; or a standard designator, optionally followed by its document number such
# as "2883-2022", "800-53" or "27001:2022"), then only four-part clause numbers
# joined by list separators (a comma, "and", "or", "to", "through", a hyphen or an
# en dash), so a later item of a continuing list keeps the cue. A list item must be
# a four-part number: a shorter section or document number ("section 4 to",
# "section 4.2 to", "RFC 5737,") does not carry the cue on to a following address.
_CLAUSE_NUMBER = r"\d+(?:\.\d+){3}"
_CLAUSE_LIST_SEP = r"(?:\s*,\s*(?:(?:and|or)\s+)?|\s+(?:and|or|to|through)\s+|\s*[-\u2013]\s*)"
CITATION_CUE_RE = re.compile(
    r"(?:\u00a7\u00a7?\s*"
    r"|(?:\b(?i:sections?|clauses?)|\b(?:IEEE|ISO/IEC|ISO|IEC|NIST|SP|RFC)(?:\s+\d[\w:/-]*)?)\s+)"
    rf"(?:{_CLAUSE_NUMBER}{_CLAUSE_LIST_SEP})*$"
)
# A port (":53") or a CIDR prefix length ("/0" to "/32", including one that ends a
# sentence) right after the match, or a URL scheme in the same token before it,
# marks a network address, never a clause number, whatever cue precedes it.
_ADDRESS_SUFFIX_RE = re.compile(r":\d|/(?:3[0-2]|[12]?\d)(?!\d|\.\d)")
_URL_PREFIX_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.\-]*://\S*$")


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


def is_citation_ip(line: str, start: int, end: int) -> bool:
    """Heuristic: is the IP-shaped match a standard clause number in a citation?

    Clause numbers like "8.2.2.1" can match the IPv4 regex. If the match sits
    directly after a citation cue, or later in a list of clause numbers that a cue
    opens (see ``CITATION_CUE_RE``), treat it as a clause number, not an IP. A port
    or CIDR suffix after the match, or a URL scheme before it, keeps it an address.
    No octet-range check is needed here: ``is_documentation_ip`` already skips a
    match that does not parse as an IPv4 address, such as one with an octet over 255.
    """
    if _ADDRESS_SUFFIX_RE.match(line, end):
        return False
    prefix = line[:start]
    if not CITATION_CUE_RE.search(prefix):
        return False
    return not _URL_PREFIX_RE.search(prefix)


# Domain-label separators, including the Unicode "dot" variants that IDN / browsers
# normalise to ".": ideographic full stop, fullwidth full stop, halfwidth ideographic
# full stop.
_DOMAIN_DOTS = (".", "。", "．", "｡")


def _idna_label_continues(c: str) -> bool:
    """Exact UTS-46: True iff codepoint ``c`` could be part of a valid domain LABEL in
    some context (retain -> keep scanning; the email is NOT a complete reserved/example
    domain). False ONLY when ``c`` cannot begin or continue any valid label (a boundary).

    FALSE-NEGATIVE-SAFE. A single codepoint cannot be settled by encoding it in isolation,
    because some valid label characters are valid only in COMPOSITION: a conjoining Hangul
    jamo (U+1100) or a combining mark is rejected by ``idna.encode`` on its own yet forms a
    valid label when composed with its neighbours (``a.test.\uac01.com`` is a real IDN
    domain). So every LETTER, MARK, or NUMBER (Unicode general category L*/M*/N*) is
    retained outright, covering the compositional cases without a false boundary. Only a
    punctuation, symbol, separator, or format character (P*/S*/Z*/C*) is probed with
    ``idna.encode``: a context error (a valid-in-context codepoint such as a joiner)
    retains, and only ``InvalidCodepoint`` (disallowed anywhere) is a boundary. Verified
    against idna 3.11; ``InvalidCodepointContext`` / ``IDNABidiError`` are siblings of
    ``InvalidCodepoint`` (not subclasses), so a context error is never mis-read as a
    boundary."""
    if unicodedata.category(c)[:1] in ("L", "M", "N"):
        return True                       # letter/mark/number: a possible (compositional) label char
    try:
        idna.encode("a" + c, uts46=True, std3_rules=True)
        return True                       # encodes as a label char
    except idna.InvalidCodepointContext:
        return True                       # valid in context (joiner/bidi): FN-safe retain
    except idna.InvalidCodepoint:
        return False                      # disallowed anywhere -> a real label boundary
    except idna.IDNAError:
        return True                       # any other IDNA constraint: FN-safe retain


def _label_starts(ch: str) -> bool:
    """Whether ``ch`` could begin or continue a (possibly IDN) domain LABEL, so that an
    email match ending just before it may be a truncated prefix of a longer real domain.

    Uses EXACT UTS-46 domain-label validity via the ``idna`` package when installed (the
    primary path, ``_idna_label_continues``); when ``idna`` is absent (a bare adopter clone),
    it falls back to the FALSE-NEGATIVE-SAFE approximation described here. The D-220 QA panel
    proved this fallback is the safe MINIMAL boundary because NO Unicode-general-category
    boundary set is safe: IDNA-valid characters hide in ``Po`` (the Tibetan tsheg,
    katakana middle dot), ``Cf`` (ZWJ), ``Sk`` (U+0375) and ``So`` (U+06FD/U+06FE). So
    the boundary test is deliberately MINIMAL: after NFKC normalisation, a character is
    a boundary only when its first normalised codepoint is whitespace, a dot separator
    (handled by the caller), or an ASCII PUNCTUATION character. Every other character
    RETAINS the address for scanning: an ASCII alphanumeric or ``-`` (a normal label
    char) and every non-ASCII character (a possible IDN label char). The safety property
    is set INCLUSION, not the stronger and false claim that no IDNA character maps to
    ASCII (a fullwidth letter such as U+FF41 does NFKC-map to ASCII, but to an
    alphanumeric, which the ASCII branch retains): the only characters granted a boundary
    are whitespace, dot separators, and codepoints whose NFKC form begins with ASCII
    punctuation, and that boundary set was verified EMPIRICALLY (over every
    boundary-classified code-point, against ``idna.encode(uts46=True, std3_rules=True)``)
    to contain no character IDNA accepts as a domain-label continuation. A real (possibly
    IDN) domain whose ASCII prefix looks reserved therefore can never be wrongly exempted. Residual cost: a harmless over-flag of a
    reserved/example email placed immediately (no separating space) against an exotic
    non-ASCII symbol, curly quote, CJK bracket or zero-width character, which plain-ASCII
    fixtures never produce (ASCII spaces, quotes, brackets and punctuation stay exempt)."""
    norm = unicodedata.normalize("NFKC", ch)
    if not norm:
        return False                              # default-ignorable / empty: boundary
    c = norm[0]
    if c.isspace() or c in _DOMAIN_DOTS:
        return False
    if c == "-":
        return True
    if c.isascii():
        return c.isalnum()                        # ASCII: alnum continues, punctuation is a boundary
    return _idna_label_continues(c) if _HAVE_IDNA else True   # non-ASCII: exact UTS-46 (FN-safe fallback)


def _email_domain_complete(line: str, end: int) -> bool:
    """True when the matched email's domain is the WHOLE domain, not a prefix the ASCII
    ``EMAIL_RE`` truncated at a non-ASCII / IDN character. The reserved-suffix and
    example-domain exemptions apply only when this holds, so a real domain such as
    ``a.test.<idn>.com`` (whose ASCII prefix ``a.test`` ends in a reserved suffix) is
    not wrongly exempted. See ``_label_starts`` for the false-negative-safe design and
    its residue. A trailing boundary (EOL, whitespace, an ASCII/normalised-ASCII
    punctuation, a symbol/quote/bracket/underscore, or a sentence-ending or repeated
    dot) keeps a legitimate reserved/example address exempt."""
    if end >= len(line):
        return True
    # NFKC-normalise so a compatibility dot (U+2024, U+FE52, U+FF0E) is recognised as a
    # separator, then apply the dot look-ahead; otherwise classify the character itself.
    first = unicodedata.normalize("NFKC", line[end])[:1]
    if first in _DOMAIN_DOTS:
        after = line[end + 1] if end + 1 < len(line) else ""
        # a dot continues the domain only when a LABEL character follows it; a dot
        # followed by another dot (an ellipsis / repeated dot) or by a boundary is
        # ordinary punctuation, not a domain separator.
        return not (after != "" and _label_starts(after))
    return not _label_starts(line[end])


def scan(path: Path, *, example_domains) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        # Email addresses
        for m in EMAIL_RE.finditer(line):
            local, domain = m.group(1), m.group(2).lower()
            if (domain in example_domains or domain.endswith(RESERVED_EMAIL_SUFFIXES)) \
                    and _email_domain_complete(line, m.end()):
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
            if is_citation_ip(line, m.start(), m.end()):
                continue
            findings.append((lineno, "public IPv4 address", addr))
        # Street addresses
        for m in STREET_RE.finditer(line):
            findings.append((lineno, "postal address fragment", m.group(0)))
    return findings
