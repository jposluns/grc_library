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
    when it is exactly part of one of four git remote forms, and only when
    the whole whitespace-delimited token that contains it is exactly that
    form: git@github.com:OWNER/REPO, ssh://git@github.com/OWNER/REPO,
    git@gitlab.com:OWNER/REPO or ssh://git@gitlab.com/OWNER/REPO, where
    OWNER and REPO are one or more ASCII letters, digits, dots, underscores
    and hyphens (so REPO may end in .git) joined by exactly one "/". The
    token starts at the start of a physical line or after an ASCII space or
    tab, and is followed by an ASCII space, a tab or the end of the line,
    or by exactly one of . , ; : ) and then one of those. Such a remote
    names a hosting service's shared login, not a person; the user and host
    are exact and case-sensitive. Every other match, whatever precedes or
    follows it, is reported as before: a bare address with no repository
    path, a form split across lines, a deeper path (group/sub/repo), a form
    inside or after any other character (a parenthesis, an angle bracket, a
    quote, an HTML tag or comment, a non-ASCII space or any other non-ASCII
    character, another URI scheme such as https:// or mailto:, or a carriage
    return in the same token, such as one right after the remote at the end
    of a CRLF line), another user at github.com or
    gitlab.com, ``git`` at any other domain, a near-miss host, and a longer
    domain that begins with ``github.com``.
    So a match right after @ (user@git@github.com or user@git@gitlab.com) is
    still reported, because the engine reports only its git@ suffix and that
    suffix is the end of a longer address, not a whole local part; and an
    address wrapped in backticks or single quotes (a Markdown code span such
    as `git@github.com`, or 'git@gitlab.com') is still reported by the token
    rule, since the backtick or apostrophe is part of its token; both are
    RFC 5322 local-part characters, so the match may be the end of a longer
    local part and the allowance fails closed. An address right after a
    double quote is still reported by the token rule. A token the rule admits is also still reported when a
    double quote appears anywhere after the match on the line, and so is an
    address after any other character (white space, a parenthesis, ssh:// or
    the start of the line included) when one does, because a double quote
    can open an RFC 5322 quoted local part, which can hold white space, and
    white space, a comment or a folded line break can separate its closing
    quote from the @ after it, so the match may be inside a longer address
    at another domain.
    Lines and paragraphs: the allowance reads the file without newline
    translation and splits it into physical lines at LF only, so a carriage
    return, form feed, vertical tab, U+0085, U+2028 or U+2029 does not end a
    line (and is not a token delimiter). A paragraph is a run of physical
    lines up to the next line that holds no character at all; a line of
    only white space does not end it, because an obsolete RFC 5322 fold can
    continue across such a line. An admitted token is still refused when
    any of these holds within its paragraph. A quote mark appears anywhere
    after the match in the rest of its paragraph: a double quote, a
    character whose NFKC form is one, or a character reference that renders
    a double quote or an apostrophe (&quot;, &apos; or a decimal or
    hexadecimal reference to 34 or 39, in any letter case, with any leading
    zeros, with or without its final semicolon), since a quoted local part
    can be folded and close on a later line. The run before the token holds
    a refusing character. That run is found by walking back from the token
    over white space, line breaks, Markdown block quote markers and every
    character that, after NFKC normalization and after decoding character
    references, is neither a letter, a digit nor white space (so any inline
    marker: the Markdown delimiters *, _, `, ~, == and ^, a fullwidth
    asterisk, &ast; or &#42;, or a bracket that a later character closes
    after the token), up to the nearest letter or digit, which is tested
    too. A refusing character is a dot, a closing parenthesis, a character
    whose NFKC form is either, or the end of a character reference (any
    reference refuses, whatever it renders), the end of an HTML tag or
    comment (a ">" that is not a block quote marker), or a character whose
    NFKC form holds a dot or a closing parenthesis (such as U+2488 or
    U+2474), since an obsolete local part such as alice. git@github.com:o/r,
    alice.<!----> git@github.com:o/r, **alice.** git@github.com:o/r or
    ==alice.== git@github.com:o/r (each renders as alice.
    git@github.com:o/r) is the address alice.git@github.com.
    The paragraph holds an @ sign, a character whose NFKC form is one or a
    character reference that renders one, other than the @ of a match that
    passes every other test here; then every match in the paragraph is
    refused, since a longer address that holds an admitted token inside a
    quoted string, a comment or a domain literal, which may all hold white
    space (x( git@github.com:o/r )@corp.example or
    user@[ git@github.com:o/r ]), needs a second @. With these refusals no
    quoting, spacing, comment or folding form can hide a second address
    around an allowed match, since RFC 5322 folding never crosses a line
    that holds no character. The accepted over-refusal: an allowed address
    followed later on the line by any double quote is reported, even when
    the match is the whole local part, and so is one followed by a quote
    mark later in its paragraph, one after a sentence-ending dot, a closing
    parenthesis or an HTML tag, even with other punctuation or a line break
    between (Clone it. git@github.com:o/r or Clone it. - git@github.com:o/r),
    every remote
    in a paragraph that holds any other @, and every remote whose token
    holds a carriage return. A carriage return is not a token delimiter, so
    a remote at the end of a CRLF line (git@github.com:o/r, then CR and LF)
    is reported, but one followed by an ASCII space or tab before the
    carriage return (git@github.com:o/r, a space, then CR and LF) still
    passes the token rule, since the space or tab ends its token first.
    Write a remote as one of the four forms, alone in its token on one
    physical line, with no dot, closing parenthesis or tag before it (even
    behind any run of inline markers or other punctuation) and no quote mark after it or
    other @ anywhere in its paragraph.
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
import bisect
import re
import sys
import unicodedata
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

# The only two addresses the git remote form allowance can cover. The rule and why: see
# "Git remote forms" in the module docstring.
FORGE_SERVICE_ADDRESSES = frozenset({"git@github.com", "git@gitlab.com"})
# The four remote forms as one whole-token pattern, and the token delimiters. Group "ssh" or
# "scp" is the user and host, the engine's match. The rule and why: see "Git remote forms" in
# the module docstring.
_REMOTE_TOKEN_RE = re.compile(
    r"(?:ssh://(?P<ssh>git@(?:github|gitlab)\.com)/|(?P<scp>git@(?:github|gitlab)\.com):)"
    r"[A-Za-z0-9._\-]+/[A-Za-z0-9._\-]+[.,;:)]?"
)
_TOKEN_DELIMITERS = " \t"
# A quote mark: a double quote, a character whose NFKC form is one (U+FF02), or a character
# reference that renders a double quote or an apostrophe, in any letter case, with any leading
# zeros and with or without its final semicolon. The rule and why: see "Git remote forms" in
# the module docstring.
_QUOTE_RE = re.compile(r'["\uff02]|&(?:quot|apos|#0*3[49]|#x0*2[27]);?', re.IGNORECASE)
# An @ sign: the character itself, a character whose NFKC form is one (U+FE6B, U+FF20), or a
# character reference that renders one. The rule and why: see "Git remote forms" in the
# module docstring.
_AT_RE = re.compile(r"[@\ufe6b\uff20]|&(?:commat|#0*64|#x0*40);?", re.IGNORECASE)
# A character reference ending at the end of the searched text. The rule and why: see "Git
# remote forms" in the module docstring.
_REFERENCE_END_RE = re.compile(r"&(?:#[0-9]+|#x[0-9a-f]+|[a-z][a-z0-9]*);?\Z", re.IGNORECASE)


def _local_part_complete(line: str, start: int) -> bool:
    """True when the match at ``start`` can be taken as the whole local part of a git remote.

    The whole token that holds it (_TOKEN_DELIMITERS) must be exactly one of the four forms
    (_REMOTE_TOKEN_RE) with the match as its user and host. False too when a double quote
    appears anywhere after the match on the line (or another quote mark, _quote_follows), an
    accepted over-refusal. The rule and why: see "Git remote forms" in the module docstring.
    """
    if _quote_follows(line[start:]):
        return False
    first = max(line.rfind(c, 0, start) for c in _TOKEN_DELIMITERS) + 1
    ends = [i for i in (line.find(c, start) for c in _TOKEN_DELIMITERS) if i >= 0]
    m = _REMOTE_TOKEN_RE.fullmatch(line, first, min(ends, default=len(line)))
    return m is not None and m.start(m.lastgroup) == start


def _quote_follows(text: str) -> bool:
    """True when ``text`` holds a quote mark (_QUOTE_RE): a double quote, a character whose
    NFKC form is one, or a character reference that renders a double quote or an apostrophe."""
    return _QUOTE_RE.search(text) is not None


def _local_part_continues_before(text: str, pos: int) -> bool:
    """True when the run before ``pos`` holds a refusing character. The run is the white space,
    the Markdown block quote markers (a ">" with only white space and ">" before it on its line)
    and every character whose NFKC form holds no letter or digit, back to the nearest character
    whose NFKC form holds one, which is tested too. A refusing character is one whose NFKC form
    holds a dot or a closing parenthesis, the end of a character reference (_REFERENCE_END_RE),
    or any other ">". The rule and why: see "Git remote forms" in the module docstring."""
    i = pos
    while i > 0:
        char = text[i - 1]
        if char.isspace():
            i -= 1
            continue
        line_start = text.rfind("\n", 0, i) + 1
        if char == ">" and not text[line_start:i].strip(" \t>"):
            i = line_start
            continue
        if char == ">" or _REFERENCE_END_RE.search(text, max(text.rfind("&", 0, i), 0), i):
            return True
        form = unicodedata.normalize("NFKC", char)
        if "." in form or ")" in form:
            return True
        if any(c.isalnum() for c in form):
            return False
        i -= 1
    return False


def _paragraphs(text: str) -> list[tuple[int, str]]:
    """``(offset, paragraph)`` for each run of LF-delimited physical lines that hold at least
    one character. Only LF ends a line, and only a line with no character at all ends a
    paragraph: a line of only white space, a carriage return, a form feed, a vertical tab,
    U+0085, U+2028 and U+2029 do not."""
    result = []
    start = None
    offset = 0
    for line in text.split("\n"):
        if line == "":
            if start is not None:
                result.append((start, text[start:offset - 1]))
                start = None
        elif start is None:
            start = offset
        offset += len(line) + 1
    if start is not None:
        result.append((start, text[start:]))
    return result


def _allowed_spans(engine, paragraph: str) -> list[tuple[int, int]]:
    """The ``(start, end)`` offsets in ``paragraph`` of the matches the git remote form
    allowance covers. Each is an engine EMAIL_RE match on one LF-delimited physical line whose
    text is exactly one of FORGE_SERVICE_ADDRESSES, that is the user and host of a whole
    whitespace-delimited token that is exactly one git remote form, with no quote mark after it
    on its line (_local_part_complete) or on a later line of the paragraph (_quote_follows), and
    no dot, closing parenthesis, tag or character reference before its token
    (_local_part_continues_before). When the paragraph holds any @ sign (_AT_RE) other than
    the @ of such a match, no match in it is covered. The rule and why: see "Git remote forms" in the module docstring."""
    spans = []
    offset = 0
    for line in paragraph.split("\n"):
        for m in engine.EMAIL_RE.finditer(line):
            start, end = m.start(), m.end()
            lead = start - len("ssh://") if line[:start].endswith("ssh://") else start
            if (m.group(0) in FORGE_SERVICE_ADDRESSES and _local_part_complete(line, start)
                    and not _quote_follows(paragraph[offset + len(line):])
                    and not _local_part_continues_before(paragraph, offset + lead)):
                spans.append((offset + start, offset + end))
        offset += len(line) + 1
    own_at = {start + len("git") for start, _ in spans}
    if any(m.start() not in own_at for m in _AT_RE.finditer(paragraph)):
        return []
    return spans


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
    one per covered match on the same engine line. The allowance reads the file itself
    without newline translation and works on LF-delimited physical lines and paragraphs
    (_paragraphs, _allowed_spans); each covered match is mapped back to the engine's line
    number, which splits at every line break str.splitlines knows. The engine's lines and
    the untranslated text's str.splitlines lines are the same lines.
    """
    engine = _engine()
    findings = engine.scan(path, example_domains=EXAMPLE_DOMAINS)
    if not any(label == "email address" and value in FORGE_SERVICE_ADDRESSES
               for _, label, value in findings):
        return findings
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return findings
    line_starts = []
    position = 0
    for piece in text.splitlines(keepends=True):
        line_starts.append(position)
        position += len(piece)
    allowed: dict[tuple[int, str], int] = {}
    for offset, paragraph in _paragraphs(text):
        for start, end in _allowed_spans(engine, paragraph):
            lineno = bisect.bisect_right(line_starts, offset + start)
            value = paragraph[start:end]
            allowed[(lineno, value)] = allowed.get((lineno, value), 0) + 1
    kept = []
    for lineno, label, value in findings:
        if label == "email address" and allowed.get((lineno, value), 0) > 0:
            allowed[(lineno, value)] -= 1
            continue
        kept.append((lineno, label, value))
    return kept


def _forge_service_matches(engine, line: str, following: str = "") -> list[str]:
    """The matches on one physical line that the git remote form allowance covers, when
    ``following`` is the rest of its paragraph (the line opens the paragraph): an engine
    EMAIL_RE match whose text is exactly one of FORGE_SERVICE_ADDRESSES, that is the user and
    host of a whole whitespace-delimited token that is exactly one git remote form, with no
    quote mark after it on the line (_local_part_complete) or in ``following``
    (_quote_follows), no dot, closing parenthesis, tag or character reference before its
    token (_local_part_continues_before), and no other @ sign in the paragraph
    (_allowed_spans). The rule and why: see "Git remote forms" in the module docstring."""
    paragraph = line + "\n" + following if following else line
    return [paragraph[start:end] for start, end in _allowed_spans(engine, paragraph)
            if end <= len(line)]


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
