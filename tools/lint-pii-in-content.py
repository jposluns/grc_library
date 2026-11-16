#!/usr/bin/env python3
"""Detect personal identifiable information (PII) patterns in library content.

The library is meant to be organization-neutral and individual-neutral.
Personal data in openly-published (CC BY-SA 4.0) content is a privacy issue: anyone
adopting the library inherits whatever names, emails, phone numbers,
or addresses appear in the source. This linter defends against
sanitization gaps.

Patterns detected:
- Email addresses (other than maintainer contact files and example
  domains).
- US Social Security Number patterns (3-2-4 digit form).
- US phone numbers (10-digit forms with separators).
- Plausible postal-address fragments (street number + street name).
- IPv4 addresses outside RFC 1918 / documentation ranges (10/8,
  172.16/12, 192.168/16, 127/8, 169.254/16, 192.0.2/24, 198.51.100/24,
  203.0.113/24); also multicast, reserved, unspecified, 0.0.0.0/8,
  255.255.255.0/24, and CGNAT 100.64.0.0/10 addresses, and an
  unparseable address (treated as documentation).

The linter is deliberately conservative on email and addresses to
avoid false positives on documentation examples.

Exemption layers:

  - EXAMPLE_DOMAINS: reserved/documentation domains (``example.com``,
    ``example.org``, ``example.net``, ``test``, ``localhost``,
    ``invalid``), adopter placeholders (``yourcompany.com``,
    ``your-org.com``, ``your-org.example.com``), threat-scenario
    placeholders (``competitor.com``, ``attacker.com``, ``evil.com``,
    ``phishing.example``, ``malicious.example``), and ``posluns.ca``
    (the maintainer's contact address, kept available for adopter
    contact) are not flagged.
  - Reserved TLDs (engine ``RESERVED_EMAIL_SUFFIXES``): email addresses
    on the RFC 2606 / RFC 6761 reserved suffixes (``.invalid``,
    ``.test``, ``.example``, ``.localhost``) are not flagged, matched as
    a suffix and only when the ASCII regex captured the whole domain.
  - Version-string heuristic: IPv4-shaped strings that look like
    software versions (e.g., ``4.0.1.2`` adjacent to "v" or "version"
    or "Rev") are treated as version numbers, not addresses.
  - Clause-citation context: a four-part standard clause number
    directly after a section sign, "section(s)", "clause(s)" or a
    standard designator (IEEE, ISO/IEC, ISO, IEC, NIST, SP, RFC), or
    later in a list of four-part clause numbers one of those opens
    (a designator may carry its document number), is treated
    as a citation, not an address. A match with a port, a CIDR suffix
    or a URL scheme is still reported.
  - Per-file exemptions: a small set of AI security guides and
    research notes whose content legitimately includes IP-shaped
    threat indicators or address examples.
  - Git remote forms (FORGE_SERVICE_ADDRESSES, maintainer decisions
    2026-11-15 and 2026-11-16): an address-shaped match is allowed only
    when it is exactly part of one of four git remote forms followed by a
    repository path on the same line: ``git@github.com:`` or
    ``git@gitlab.com:`` (scp style), or ``ssh://git@github.com/`` or
    ``ssh://git@gitlab.com/``. Such a remote names a hosting service's
    shared login, not a person. The user and host are exact and
    case-sensitive, and the engine's regex must have captured the whole
    domain. The repository path is at least owner/repository: segments of
    ASCII letters, digits, underscores, dots and hyphens, each starting
    with a letter, digit or underscore, joined by "/", ending at the end of
    the line, at white space or at one of ) ] } > , ; ' ! ? or a backtick.
    The scp form starts at the start of the line, after white space or
    after an ASCII character that cannot sit in a local part; the ssh://
    form starts at the start of the line or after an ASCII character that
    cannot sit in a URI scheme. Every other match is reported as before: a
    bare address with no repository path, a form split across lines,
    another user at github.com or gitlab.com, ``git`` at any other domain,
    a near-miss host, and a longer domain that begins with ``github.com``.
    The match must also be the whole local part (_local_part_complete): a match
    right after @ (user@git@github.com or user@git@gitlab.com) is still
    reported, because the engine reports only its git@ suffix and that
    suffix is the end of a longer address, not a whole local part;
    an address wrapped in backticks or single quotes (a Markdown code span
    such as `git@github.com`, or 'git@gitlab.com') is still reported,
    because the backtick and the apostrophe are RFC 5322 local-part
    characters, so the match may be the end of a longer local part and
    the allowance fails closed. An address right after a double quote is
    still reported when a double quote appears anywhere after the match on
    the line, and so is an address after any other character (white space, a
    parenthesis, ssh:// or the start of the line included) when one does,
    because a double quote can open an RFC 5322 quoted local part, which can
    hold white space and parentheses, and white space, a comment or a folded
    line break can separate its closing quote from the @ after it, so the
    match may be inside a longer address at another domain. A quoted local
    part can itself be folded across lines and close on a later line, so the
    allowance is also refused when a double quote, or the character
    reference &quot;, &#34; or &#x22;, appears anywhere after the match in
    the rest of its paragraph (up to the next empty line, since a fold
    always continues on a line that starts with white space). The rule looks
    for any later double quote, not for an @ after one, so no quoting,
    spacing, comment or folding form can hide a second address. The accepted
    over-refusal: an allowed address followed later on the line by any double
    quote is reported, even when the match is the whole local part, as in a
    double-quoted remote such as a string value, and so is one followed by a
    double quote later in its paragraph. After another URI scheme (an
    https:// credential such as https://git@github.com, or
    mailto:git@github.com) it is still reported, since neither is an ssh://
    or scp-style remote. Write a remote as one of the four forms with its
    repository path on one line, with no double quote after it in its
    paragraph.
  - CHANGELOG.md is exempt because it can describe sanitization fixes
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
import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import guard_explicit_paths_cwd, REPO_ROOT, iter_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

SCAN_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt", ".cff"}

# Files exempt because they intentionally contain maintainer contact info
# (CITATION.cff and AUTHORS.md) or describe PII patterns by example
# (privacy standards, the PII linter source itself).
EXEMPT_FILES = {
    "AUTHORS.md",
    "CITATION.cff",
    "lint-pii-in-content.py",
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
    # The pack-owned engine (gate_lint_pii_in_content.py) now holds the PII
    # detection regexes, so it documents the PII formats by design exactly as
    # this wrapper did before the PR-38 transfer; exempt it for the same reason.
    "gate_lint_pii_in_content.py",
    # The PR-attribution check matches the attribution trailer address by design (its
    # pattern and self-test cases document the forbidden attribution shapes).
    "check-pr-attribution.py",
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
    # Template-placeholder organization domains (see note above)
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

# Git remote forms (maintainer decisions 2026-11-15 and 2026-11-16): the SSH
# service address of a code-hosting site names the service's shared login, not a
# person, but only as the user and host of an exact git remote form with a repository
# path (_git_remote_form). Only these two exact addresses can be allowed, and a bare
# one is reported. This is not a domain allowance: any other local part at github.com
# or gitlab.com, and git at any other domain, is reported as before.
FORGE_SERVICE_ADDRESSES = frozenset({"git@github.com", "git@gitlab.com"})
# The repository path after "git@host:" or "ssh://git@host/": owner/repository at least,
# then the end of the line, white space or closing punctuation. Any other following
# character (@, :, a double quote, a non-ASCII letter and so on) means the text is not an
# exact remote form.
_REPO_PATH_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.\-]*(?:/[A-Za-z0-9_][A-Za-z0-9_.\-]*)+(?=\Z|[\s)\]}>,;'!?`])")
# Characters that may appear in a URI scheme: one directly before "ssh://" makes it
# part of another scheme (such as xssh://), not the ssh:// form.
_SCHEME_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.")
# A double quote or its HTML character reference: a quoted local part around the match
# needs one of these after it to close.
_QUOTE_MARKS = ('"', "&quot;", "&#34;", "&#x22;")
# The engine's EMAIL_RE starts a match at a word boundary, so for
# o'git@github.com or alice!git@gitlab.com it captures only the git@ suffix. The
# allowance applies only when the character before the match cannot sit in a local
# part: not an RFC 5322 atext character or dot, and not a non-ASCII character (RFC 6531),
# except whitespace, or the "/" that ends an ssh:// prefix (another scheme's "://", such
# as https://, marks a URL credential, not an SSH remote). Nor "@", which is no local-part
# character, but a match right after it (user@git@github.com) is the end of a longer
# address, not a whole local part. Nor ":", which ends a URI scheme such as mailto:.
# A double quote is no atext character, but it can open a quoted local part, which can hold
# white space and parentheses, and white space, a comment or a folded line break can separate
# its closing quote from the @ after it: whatever comes before the match, it may be inside a
# longer address when a double quote appears anywhere after it on the line, so the allowance is
# then refused. Testing for any later double quote, not for an @ after one, leaves no quoting
# form that hides a second address; the cost is that an allowed address followed later on the
# line by any double quote is reported.
_LOCAL_PART_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'*+-/=?^_`{|}~."
)


def _local_part_complete(line: str, start: int) -> bool:
    """True when the match at ``start`` can be taken as the whole local part.

    False when it may be the suffix of a longer one: after a local-part character, @ or a URI
    scheme's colon, or when a double quote appears anywhere after the match on the line, since
    that quote may close a quoted local part around it. The last test also refuses some
    matches that are whole local parts (accepted over-refusal).
    """
    if '"' in line[start:]:
        return False
    if start == 0 or line[:start].endswith("ssh://"):
        return True
    before = line[start - 1]
    if before.isspace():
        return True
    return before.isascii() and before not in "@:" and before not in _LOCAL_PART_CHARS


def _git_remote_form(line: str, start: int, end: int) -> bool:
    """True when ``line[start:end]`` is exactly the user and host of a git remote form.

    The forms are ``git@<host>:<path>`` (scp style) and ``ssh://git@<host>/<path>``, with
    the repository path (_REPO_PATH_RE) on the same line. A bare address, a form split across
    lines, a form after a local-part character (scp style) or after a URI scheme character
    (ssh://) is not one.
    """
    if end >= len(line):
        return False
    sep = line[end]
    if sep == ":":
        if start > 0:
            before = line[start - 1]
            if not before.isspace() and (not before.isascii() or before in "@:"
                                         or before in _LOCAL_PART_CHARS):
                return False
    elif sep == "/" and line[:start].endswith("ssh://"):
        lead = start - len("ssh://")
        if lead > 0:
            before = line[lead - 1]
            if not before.isspace() and (not before.isascii() or before in _SCHEME_CHARS):
                return False
    else:
        return False
    return _REPO_PATH_RE.match(line, end + 1) is not None


def _quote_follows(text: str) -> bool:
    """True when ``text`` holds a double quote or its character reference (_QUOTE_MARKS)."""
    lowered = text.lower()
    return any(mark in lowered for mark in _QUOTE_MARKS)


def _rest_of_paragraph(lines: list[str], lineno: int) -> str:
    """The lines after line ``lineno`` (one-based) up to the next empty line, joined."""
    rest = []
    for following in lines[lineno:]:
        if following == "":
            break
        rest.append(following)
    return "\n".join(rest)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_pii_in_content  # the pack-owned engine (source of record)
    return gate_lint_pii_in_content


def scan(path: Path) -> list[tuple[int, str, str]]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression
    test patches ``mod.scan`` and runs ``main``; the detection regexes and the
    check live in the pack engine (gate_lint_pii_in_content.py). The engine takes
    the grc example-domain allow-list as a keyword; the wrapper supplies it here.
    The wrapper then drops the email findings the git remote form allowance covers,
    one per covered match on the same line, given the rest of that line's paragraph.
    """
    engine = _engine()
    findings = engine.scan(path, example_domains=EXAMPLE_DOMAINS)
    if not any(label == "email address" and value in FORGE_SERVICE_ADDRESSES
               for _, label, value in findings):
        return findings
    allowed: dict[tuple[int, str], int] = {}
    text = engine.read_text_safe(path) or ""
    lines = text.splitlines()
    for lineno, line in engine.iter_non_code_lines(text):
        for value in _forge_service_matches(engine, line, _rest_of_paragraph(lines, lineno)):
            allowed[(lineno, value)] = allowed.get((lineno, value), 0) + 1
    kept = []
    for lineno, label, value in findings:
        if label == "email address" and allowed.get((lineno, value), 0) > 0:
            allowed[(lineno, value)] -= 1
            continue
        kept.append((lineno, label, value))
    return kept


def _forge_service_matches(engine, line: str, following: str = "") -> list[str]:
    """The matches on one line that the git remote form allowance covers: an engine
    EMAIL_RE match whose text is exactly one of FORGE_SERVICE_ADDRESSES, whose domain is
    the whole domain, not an ASCII prefix the regex truncated (the engine's own
    completeness rule, as for its example-domain exemption), that is exactly the user and
    host of a git remote form with a repository path (_git_remote_form), whose local part
    is the whole local part (_local_part_complete), and with no double quote or quote
    character reference after it on the line or in ``following``, the rest of its
    paragraph (_quote_follows)."""
    return [m.group(0) for m in engine.EMAIL_RE.finditer(line)
            if m.group(0) in FORGE_SERVICE_ADDRESSES and engine._email_domain_complete(line, m.end())
            and _git_remote_form(line, m.start(), m.end())
            and _local_part_complete(line, m.start())
            and not _quote_follows(line[m.end():] + "\n" + following)]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect PII patterns in library content."
    )
    parser.add_argument("paths", nargs="*", default=None)
    args = parser.parse_args(argv[1:])
    # 3b48: explicit paths are refused when missing or outside this tree, else normalized.
    args.paths = guard_explicit_paths_cwd(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS
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
        "openly published under CC BY-SA 4.0 and meant to be individual-neutral; replace any real PII with "
        "documentation-example placeholders or move maintainer contact to "
        "AUTHORS.md / CITATION.cff."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
