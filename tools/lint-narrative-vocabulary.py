#!/usr/bin/env python3
"""Narrative vocabulary gate (P-1.25 Phase 1.3; spec Gates item 6).

String-level vocabulary enforcement for the narrative layer, scoped to the
root ``executive/`` tree, per ``specification-executive-narrative.md``
("Causal vocabulary", "The qualified-shall rule", "Language and neutrality
requirements", Gates item 6). The existing bare-shall, language, and dash
gates do NOT cover ``executive/`` (and must not: an ``AUDITED_DOMAIN_DIRS``
edit would wrongly pull the narrative tree into every content gate), so this
gate is the narrative layer's own wiring.

Three checks, each a string-level property (the semantic halves, e.g. which
sentences are causal statements or whether a quotation is faithful, are
review outcomes the spec explicitly leaves to review):

  1. ABSOLUTES DENYLIST (page-wide, no causal-statement classification):
     ``guarantee``, ``eliminates``, ``makes impossible``, ``removes all
     risk`` must not appear in narrative prose at all. Inflections are
     matched (guarantees / guaranteed / eliminating / removing all risk):
     a fail-closed reading of the denylist, since an inflected absolute is
     the same absolute. No quotation exemption: the spec grants none for
     absolutes (unlike ``shall``), so a blockquote hit still fails.
  2. QUALIFIED-SHALL RULE: no unqualified ``shall``. The sole exception is
     the spec's qualified-shall definition, a verbatim attributed source
     quotation with VISIBLE SOURCE ADJACENCY, mechanised as:
       - an inline double-quoted span (straight or curly quotes) containing
         the ``shall``, with a citation (a markdown link or a named external
         standard) within ``ADJACENCY_WINDOW`` characters immediately before
         the opening or after the closing quote on the same line; or
       - a markdown blockquote line containing the ``shall``, with a
         citation on the blockquote line itself or on the immediately
         adjacent non-blank line (the attribution line).
     Hyphenated identifiers (``lint-shall-near-uncertainty.py``) and
     backticked word-references never match (same boundaries as gate 56).
     This proves the string-level property only; quotation faithfulness is
     a review concern (spec, "The qualified-shall rule").
  3. DASH BAN: no em (U+2014) or en (U+2013) dashes in narrative prose.
     Inline code spans and fenced blocks are exempt (a dash there is a code
     example or functional form, matching the gate-83 treatment).

Scope: EVERY ``.md`` under the root ``executive/`` tree, INCLUDING the
entry-point ``executive/README.md``. The entry-point exemption is scoped to
gates that require narrative-PAGE form (the spec's consistent-exemption list
names the boundary, metadata, disclaimer, registry, and listing gates); the
vocabulary rules are page-wide string properties of narrative-layer prose,
and the README is narrative-layer prose. An empty page set (executive/
absent, or holding only a clean README) exits 0.

Usage:
    python3 tools/lint-narrative-vocabulary.py [paths...]
    python3 tools/lint-narrative-vocabulary.py --self-test

Exit 0 on no findings; exit 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import (
    CODE_SPAN_RE,
    CROSS_EXTERNAL_CONTEXT_RE,
    REPO_ROOT,
    is_fence_line,
    read_text_safe,
)

# Bare ``shall``: free-standing, not part of a hyphenated identifier and not
# a substring (``Marshall``). Same boundaries as gate 56.
BARE_SHALL = re.compile(r"(?<![A-Za-z0-9_-])shall(?![A-Za-z0-9_-])", re.IGNORECASE)

# The absolutes denylist (spec, "Causal vocabulary"): the listed words plus
# their inflections. Lookbehind blocks hyphenated-identifier matches.
# Single-word absolutes: one token, cannot span a soft line break (checked per line).
ABSOLUTES_SINGLE: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("guarantee", re.compile(r"(?<![\w-])guarantee\w*", re.IGNORECASE)),
    ("eliminates", re.compile(r"(?<![\w-])eliminat\w*", re.IGNORECASE)),
)
# Multi-word absolutes: the phrase can wrap across a soft line break, so these are
# checked against the per-PARAGRAPH joined non-code text, not a single line.
ABSOLUTES_MULTI: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("makes impossible", re.compile(r"(?<![\w-])makes?\s+(?:\w+\s+){0,2}impossible", re.IGNORECASE)),
    ("removes all risk", re.compile(r"(?<![\w-])remov\w*\s+all\s+risk", re.IGNORECASE)),
)

# Em / en dash (functional escapes, not literal glyphs, per the tools/ dash ban).
DASH_RE = re.compile("[\u2014\u2013]")

# Inline quotation spans: straight or curly double quotes.
QUOTE_SPAN_RES: tuple[re.Pattern[str], ...] = (
    re.compile(r'"[^"]+"'),
    re.compile("\u201c[^\u201d]+\u201d"),
)

# A visible source citation: a markdown link, or a named external standard
# (the shared external-standard vocabulary from lint_common, e.g. ISO, NIST,
# GDPR). Residue: an unlinked source name outside that vocabulary does not
# qualify; authors cite qualified quotes with a link or a named standard.
MD_LINK_RE = re.compile(r"\[[^\]]*\]\([^)]+\)")

# How close (characters, same line) a citation must sit to the quotation to
# count as "visibly adjacent (inline, immediately before or after)".
ADJACENCY_WINDOW = 120


def _has_citation(segment: str) -> bool:
    return bool(MD_LINK_RE.search(segment) or CROSS_EXTERNAL_CONTEXT_RE.search(segment))


def _noncode_lines(text: str) -> list[tuple[int, str]]:
    """Non-code (lineno, raw) lines, fence-MARKER-aware: a fenced block opened by
    ``` closes only on ```, and one opened by ~~~ only on ~~~, so a mismatched
    marker inside a block (``` inside a ~~~ fence) is content, not a toggle."""
    out: list[tuple[int, str]] = []
    fence: str | None = None  # the 3-char marker (``` or ~~~) that opened the block
    for lineno, raw in enumerate(text.splitlines(), 1):
        stripped = raw.lstrip()
        marker = stripped[:3] if (stripped.startswith("```") or stripped.startswith("~~~")) else None
        if fence is None:
            if marker is not None:
                fence = marker
                continue
            out.append((lineno, raw))
        else:
            if marker == fence:
                fence = None
            # any line while inside a fence (matching-close included) is code: skip
    return out


def _shall_is_qualified(line: str, match: re.Match[str], idx: int,
                        noncode: list[tuple[int, str]]) -> bool:
    """The qualified-shall test (see module docstring). ``line`` is the
    code-span-stripped line; ``idx`` indexes ``noncode`` for blockquote
    adjacency."""
    if line.lstrip().startswith(">"):
        # Blockquote quotation: citation on the line or an adjacent non-blank line.
        if _has_citation(line):
            return True
        for step in (-1, 1):
            j = idx + step
            while 0 <= j < len(noncode) and not noncode[j][1].strip():
                j += step
            if 0 <= j < len(noncode) and _has_citation(noncode[j][1]):
                return True
        return False
    for qre in QUOTE_SPAN_RES:
        for qm in qre.finditer(line):
            if qm.start() < match.start() and match.end() <= qm.end():
                before = line[max(0, qm.start() - ADJACENCY_WINDOW):qm.start()]
                after = line[qm.end():qm.end() + ADJACENCY_WINDOW]
                if _has_citation(before) or _has_citation(after):
                    return True
    return False


def scan_page_text(text: str) -> list[tuple[int, str, str]]:
    """(lineno, class, message) findings for one page. PURE.

    Classes: ``absolute``, ``shall``, ``dash``."""
    findings: list[tuple[int, str, str]] = []
    noncode = _noncode_lines(text)
    for idx, (lineno, raw) in enumerate(noncode):
        stripped = CODE_SPAN_RE.sub("", raw)  # backticked word-references never match
        if DASH_RE.search(stripped):
            findings.append((lineno, "dash",
                             "em/en dash in narrative prose (the dash ban applies to the "
                             "narrative layer; rewrite with commas, colons, or parentheses)"))
        for name, pat in ABSOLUTES_SINGLE:
            if pat.search(stripped):
                findings.append((lineno, "absolute",
                                 f"absolute {name!r} in narrative prose (page-wide denylist; a "
                                 f"narrative page states contribution, dependency, prevention, "
                                 f"or evidence, never an absolute)"))
        for m in BARE_SHALL.finditer(stripped):
            if _shall_is_qualified(stripped, m, idx, noncode):
                continue
            findings.append((lineno, "shall",
                             "unqualified 'shall' (narrative prose harmonizes on 'must'; a "
                             "'shall' is permitted only inside a verbatim quotation with a "
                             "visibly adjacent source citation)"))
    # Multi-word absolutes: scan each PARAGRAPH (consecutive non-code, non-blank
    # lines) joined with a space, so a phrase wrapped across a soft line break
    # cannot escape; report at the paragraph's first line. Paragraph-bounded (not
    # whole-page) so two unrelated sentences are not falsely joined into a match.
    para: list[tuple[int, str]] = []
    def _flush_para() -> None:
        if not para:
            return
        joined = " ".join(t for _, t in para)
        for name, pat in ABSOLUTES_MULTI:
            if pat.search(joined):
                findings.append((para[0][0], "absolute",
                                 f"absolute {name!r} in narrative prose (page-wide denylist; a "
                                 f"narrative page states contribution, dependency, prevention, "
                                 f"or evidence, never an absolute)"))
    for lineno, raw in noncode:
        stripped = CODE_SPAN_RE.sub("", raw)
        if stripped.strip():
            para.append((lineno, stripped))
        else:
            _flush_para(); para = []
    _flush_para()
    return findings


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        # Fail LOUD, not open: an executive/ page that cannot be read cannot be
        # cleared of the vocabulary rules (the 1.3a fail-loud lesson).
        return [f"{rel}: not readable / not utf-8 (cannot be checked for the narrative vocabulary rules; fail loud)"]
    return [f"{rel}:L{lineno}: {msg}" for lineno, _cls, msg in scan_page_text(text)]


def discover(root: Path = REPO_ROOT) -> list[Path]:
    exec_root = root / "executive"
    if not exec_root.is_dir():
        return []
    return sorted(p for p in exec_root.rglob("*.md") if p.is_file())


def _self_test() -> int:
    failures: list[str] = []

    def classes(text: str) -> list[str]:
        return [cls for _, cls, _ in scan_page_text(text)]

    def expect(name: str, text: str, want: list[str]) -> None:
        got = classes(text)
        if got != want:
            failures.append(f"{name}: expected classes {want}, got {got}")

    # Absolutes: base words, inflections, phrase variants.
    expect("absolute-guarantee", "The control guarantees the outcome.\n", ["absolute"])
    expect("absolute-guaranteed", "Delivery is guaranteed by the gate.\n", ["absolute"])
    expect("absolute-eliminates", "This eliminates the risk.\n", ["absolute"])
    expect("absolute-eliminating", "Eliminating the class of failure entirely.\n", ["absolute"])
    expect("absolute-makes-impossible", "The gate makes a leak impossible.\n", ["absolute"])
    expect("absolute-make-it-impossible", "Controls make it impossible to bypass review.\n", ["absolute"])
    expect("absolute-removes-all-risk", "Adoption removes all risk of drift.\n", ["absolute"])
    # No quotation exemption for absolutes: a blockquote hit still fails.
    expect("absolute-blockquote-still-flagged", "> ISO 31000: adoption guarantees outcomes.\n", ["absolute"])
    # Word-reference and fenced forms are exempt; approved causal words pass.
    expect("absolute-backtick-pass", "The word `guarantee` is banned.\n", [])
    expect("absolute-fenced-pass", "```\nguarantees\n```\n", [])
    expect("causal-vocab-pass", "The register is a contribution to, and evidence for, assurance.\n", [])

    # Qualified-shall rule.
    expect("shall-bare", "The organization shall maintain a register.\n", ["shall"])
    expect("shall-sentence-initial", "Shall we proceed with the review?\n", ["shall"])
    expect("shall-quoted-source-before", 'ISO 27001 states: "The organization shall determine the scope."\n', [])
    expect("shall-quoted-source-after", '"The organization shall determine the scope." (ISO 27001, clause 4.3)\n', [])
    expect("shall-quoted-link-adjacent", '"Access shall be revoked." per [the standard](../standards/example-standard.md).\n', [])
    expect("shall-quoted-no-source", '"The organization shall determine the scope."\n', ["shall"])
    expect("shall-curly-quoted-source", "NIST SP 800-53 requires: \u201cAccess shall be reviewed.\u201d\n", [])
    expect("shall-blockquote-attributed-same-line", "> GDPR Article 32: processing shall be secured.\n", [])
    expect("shall-blockquote-attribution-adjacent", "From ISO 22301:\n\n> The organization shall establish a BCMS.\n", [])
    expect("shall-blockquote-unattributed", "> The organization shall establish a BCMS.\n\nPlain prose follows.\n", ["shall"])
    expect("shall-hyphenated-identifier-pass", "See lint-shall-near-uncertainty.py for gate 9.\n", [])
    expect("shall-substring-pass", "Marshall reviewed the plan.\n", [])
    expect("shall-backtick-pass", "The word `shall` is harmonized to `must`.\n", [])

    # Dash ban.
    expect("dash-em-flagged", "Risk\u2014the board's concern\u2014is framed here.\n", ["dash"])
    expect("dash-en-flagged", "See items 1\u20133 above.\n", ["dash"])
    expect("dash-backtick-pass", "The glyphs `\u2014` and `\u2013` are banned.\n", [])
    expect("dash-fenced-pass", "```\na \u2014 b\n```\n", [])

    # Multi-class line ordering (dash, then absolute, then shall).
    expect("multi-class", "It guarantees success \u2014 and shall be adopted.\n",
           ["dash", "absolute", "shall"])

    # F1: a multi-word absolute wrapped across a soft line break must not escape.
    expect("absolute-makes-impossible-softbreak", "The control makes\nit impossible to bypass review.\n", ["absolute"])
    # F3: a mismatched fence marker inside a fenced block must not toggle out, so
    # prose after the block is still scanned.
    expect("absolute-mixed-fence-noescape", "~~~\n```\nexample\n~~~\nThe control guarantees success.\n", ["absolute"])

    # File-level fail-loud: an unreadable / non-UTF-8 page is flagged, not skipped.
    import tempfile
    with tempfile.TemporaryDirectory() as _td:
        _bin = Path(_td) / "brief-binary.md"
        _bin.write_bytes(b"\xff\xfe not utf-8 \x00")
        if not any("not readable" in f for f in check_file(_bin, "executive/brief-binary.md")):
            failures.append("unreadable-failloud: expected a 'not readable' finding, got none")

    if failures:
        for fl in failures:
            print(f"  SELF-TEST FAIL: {fl}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all vocabulary cases passed (absolutes denylist incl. inflections and "
          "no-quotation-exemption; qualified-shall inline/blockquote adjacency forms; dash ban "
          "with code-span/fence exemptions).")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv[1:]:
        return _self_test()
    args = [a for a in argv[1:] if not a.startswith("-")]
    files = [Path(a).resolve() for a in args] if args else discover()
    all_findings: list[str] = []
    for f in files:
        try:
            rel = f.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel = f.as_posix()
        all_findings.extend(check_file(f, rel))
    if all_findings:
        for finding in all_findings:
            print(f"  {finding}")
        print(f"FAIL: {len(all_findings)} narrative-vocabulary finding(s) across "
              f"{len(files)} file(s).")
        return 1
    print(f"OK: {len(files)} narrative file(s) checked; no absolutes, no unqualified "
          f"'shall', no em/en dashes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
