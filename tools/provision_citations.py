"""Statute-provision citation extractor shared by the provision-restatement tools.

A clause of a statute (PIPEDA s. 10.1, GDPR Art. 33) is often restated on
several corpus surfaces. When one surface is corrected, the others keep the
old wording unless a reviewer finds them, and reviewers tend to grep the old
PHRASE rather than the PROVISION: the #2649 retro, where PIPEDA s. 10.1
qualifiers corrected on one surface survived without them on others. This
module turns every recognizable statute-section citation into a normalized
``(instrument, section)`` key so two ADVISORY tools can group surfaces by
provision:

  - ``tools/build-provision-index.py``: every surface per key, corpus-wide.
  - ``tools/audit-provision-siblings.py``: for the documents a PR changes,
    every OTHER surface citing the same provisions (for QA briefs).

Extraction model (stdlib ``re``, fenced code skipped via
``lint_common.iter_non_code_lines``):

  1. A CITATION is a section marker (``Art.``, ``Arts.``, ``Article(s)``,
     ``s.``, ``ss.``, ``Section(s)``, ``section(s)``, ``§``, ``§§``) followed
     by one or more numbers with optional letter suffixes (``55-A``, ``4a``)
     and parenthesised subdivisions, lists (including slashed lists,
     ``Art 5/6/12``) and ranges: ``s. 10.1(2) and (6)``, ``Arts. 33 to 34``,
     ``Arts. 44–49``, ``ss. 7 to 9, 11``. A bare parenthesised continuation
     (``and (6)``) attaches to the preceding section. A numeric range
     spanning at most ``MAX_RANGE_SPAN`` sections is expanded; each interior
     section carries the range as its pinpoint (``25 to 39``). A continuation
     number followed by a unit (``and 72 hours``, ``and 72-hour``,
     ``and 20%``) or shaped as a year is not absorbed.
  2. The KEY is section-level: ``PIPEDA s. 10.1(3)`` and ``PIPEDA s. 10.1(6)``
     both key to ``PIPEDA s. 10.1``; the pinpoint is kept for display.
  3. The INSTRUMENT is resolved in this order, and the tier is recorded:
       explicit  an alias directly before the marker (``GDPR Art. 33``,
                 ``PIPEDA (s. 10.1(2)``; this wins over an alias after the
                 citation) or directly after the citation (``Article 33 of
                 the GDPR``; a bracketed alias, ``Art 26 (PDPL)``, counts
                 only when the bracket closes right after the alias, so
                 ``section 3.9 (MiCA Article 35(1))`` never keys the outer
                 citation to MiCA);
       line      the nearest alias earlier on the same line (a table row),
                 only when every alias earlier on the line names ONE
                 instrument and no foreign-prefix refusal precedes the
                 citation on the line (such a refusal means an instrument
                 outside the alias table is being cited there, so the
                 line's later bare citations are plausibly its, not the
                 alias's);
       heading   the nearest enclosing heading that names exactly one
                 instrument (for a citation ON a heading line, the
                 enclosing parent headings);
       section   the last alias mentioned in the body of the innermost
                 section so far, only where no enclosing heading names a
                 DIFFERENT instrument (that conflict is refused);
       document  the single instrument named in the Document Title.
     ``Section`` and ``§`` citations are indexed only at the explicit tier:
     a bare ``Section 4.2`` or ``§6.3`` is this corpus's internal
     cross-reference form, not a statute citation. Inference is REFUSED,
     and the citation left unresolved, where the marker directly follows an
     unaliased acronym or identifier (``CCR s. 7001``, ``RTS 2025/1140
     Arts 2``), a law word optionally followed by a number (``Ley Art 33``,
     ``the Privacy Act (s. 3)``, ``Decree 356 Art. 20``) or a possessive or
     relative reference to another instrument (``its Articles 46 and 48``,
     ``whose Article 11``), or the citation is followed by ``of this Law``,
     ``of that Regulation`` or ``of <Name>``, or directly by an instrument
     word (``Article 29(7) Regulation (EU) 2018/1725``): inference there
     would attach the citation to whichever aliased instrument happened to
     be mentioned nearby.
  4. Ambiguous short names (``PDPA``, ``PDPL``, ``CPPA``, ``PIPA``,
     ``AI Act``) resolve by the last jurisdiction word within
     ``JURISDICTION_WINDOW`` characters before the alias, then by a
     jurisdiction token in the document path, else to
     ``<alias> (jurisdiction unresolved)``. An alias used as an adjectival
     compound (``GDPR-style``, ``GDPR-Article-26-style``) is not a mention.
  5. SIGNATURE PHRASES: a small seed table of phrases that restate a
     provision WITHOUT citing it (before #2649 most PIPEDA s. 10.1 surfaces
     carried no section number at all). A hit is reported with tier
     ``phrase`` as an uncited-restatement CANDIDATE, only on a non-heading
     line that carries no resolved citation, and only when the phrase's
     instrument context is the key's instrument: the nearest alias before
     the phrase on the line, else the first after it, else the heading
     chain, else the Document Title (the weaker section-body tier is not
     used for phrases).

Residue is stated in the two tools' docstrings.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from lint_common import (
    AUDITED_DOMAIN_DIRS,
    REPO_ROOT,
    iter_non_code_lines,
    iter_scan_roots_markdown,
    read_text_safe,
)

# Surfaces that restate provisions: the root README, the audited domains
# (splatted; the scan-scope parity gate forbids hardcoding the run), the
# executive pages, and the hand-authored adopter guides under docs/.
DEFAULT_SCAN_ROOTS: tuple[str, ...] = ("README.md", *AUDITED_DOMAIN_DIRS, "executive", "docs")

# Generated artefacts derive their text from sources already in scope (or,
# for the manifest, list source titles), so a hit there is not a sibling.
EXCLUDED_FILES: frozenset[str] = frozenset(
    (
        "docs/portal.md",
        "docs/maturity-scorecard.md",
        "docs/reference-acquisition-manifest.md",
    )
)

# (canonical instrument, display marker, alias spellings). Aliases are literal
# and case-sensitive, matched on alphanumeric boundaries; the longest alias at
# a position wins, so "UK GDPR" is never read as "GDPR". A deliberately small
# seed: extend it when --show-unresolved shows a frequently cited instrument
# missing (each row is one instrument; keep aliases unambiguous or move the
# name to AMBIGUOUS_ROWS).
INSTRUMENT_ROWS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("GDPR", "Art.", ("GDPR", "EU GDPR", "General Data Protection Regulation", "Regulation (EU) 2016/679")),
    ("UK GDPR", "Art.", ("UK GDPR",)),
    ("EU AI Act", "Art.", ("EU AI Act", "Regulation (EU) 2024/1689")),
    ("MiCA", "Art.", ("MiCA", "MiCAR", "Regulation (EU) 2023/1114")),
    ("DORA", "Art.", ("DORA", "Regulation (EU) 2022/2554")),
    ("NIS2", "Art.", ("NIS2", "NIS 2", "NIS 2 Directive", "Directive (EU) 2022/2555")),
    ("LGPD", "Art.", ("LGPD",)),
    ("PIPL", "Art.", ("PIPL",)),
    ("APPI", "Art.", ("APPI",)),
    ("FADP", "Art.", ("FADP", "nFADP", "revFADP")),
    ("LFPDPPP", "Art.", ("LFPDPPP",)),
    ("UU PDP", "Art.", ("UU PDP",)),
    ("KVKK", "Art.", ("KVKK",)),
    ("PIPEDA", "s.", ("PIPEDA",)),
    ("PPCDA", "s.", ("PPCDA", "Bill C-36")),
    ("AIDA", "s.", ("AIDA",)),
    ("Quebec Law 25", "s.", ("Quebec Law 25", "Law 25")),
    ("BC PIPA", "s.", ("BC PIPA",)),
    ("Alberta PIPA", "s.", ("Alberta PIPA",)),
    ("POPIA", "s.", ("POPIA",)),
    ("PAIA", "s.", ("PAIA",)),
    ("DPDPA", "s.", ("DPDPA", "DPDP Act")),
    ("Cal. Civ. Code", "s.", ("Cal. Civ. Code", "California Civil Code", "CCPA", "CPRA")),
    ("HIPAA (45 CFR)", "s.", ("HIPAA", "45 CFR", "45 C.F.R.")),
    ("SOX", "s.", ("SOX", "Sarbanes-Oxley Act", "Sarbanes-Oxley")),
)

# (ambiguous alias, display marker, ((jurisdiction, canonical instrument), ...)).
AMBIGUOUS_ROWS: tuple[tuple[str, str, tuple[tuple[str, str], ...]], ...] = (
    ("PDPA", "s.", (("Singapore", "PDPA (Singapore)"), ("Thailand", "PDPA (Thailand)"), ("Malaysia", "PDPA (Malaysia)"))),
    ("PDPL", "Art.", (("Saudi Arabia", "PDPL (Saudi Arabia)"), ("UAE", "PDPL (UAE)"), ("Vietnam", "PDPL (Vietnam)"))),
    ("CPPA", "s.", (("Canada", "CPPA (Canada)"),)),
    ("PIPA", "Art.", (("South Korea", "PIPA (South Korea)"),)),
    ("AI Act", "Art.", (("EU", "EU AI Act"),)),
)

# Lower-case jurisdiction words (in prose and in path tokens) -> jurisdiction.
JURISDICTION_WORDS: dict[str, str] = dict(
    eu="EU",
    european="EU",
    singapore="Singapore",
    thailand="Thailand",
    thai="Thailand",
    malaysia="Malaysia",
    malaysian="Malaysia",
    saudi="Saudi Arabia",
    uae="UAE",
    emirates="UAE",
    vietnam="Vietnam",
    vietnamese="Vietnam",
    canada="Canada",
    canadian="Canada",
    korea="South Korea",
    korean="South Korea",
    california="California",
)
JURISDICTION_WINDOW = 80

# (instrument, section, pattern): uncited-restatement seed phrases.
SIGNATURE_PHRASE_ROWS: tuple[tuple[str, str, str], ...] = (
    ("PIPEDA", "10.1", r"real risk of significant harm"),
    ("GDPR", "33", r"72 hours (?:of|after) (?:becoming|having become|it becomes) aware"),
)

MAX_RANGE_SPAN = 30
TIERS: tuple[str, ...] = ("explicit", "line", "heading", "section", "document")
UNRESOLVED = "unresolved"
PHRASE = "phrase"
UNRESOLVED_JURISDICTION = " (jurisdiction unresolved)"
_NEEDS_CONTEXT = "context"

MARKER_STYLE: dict[str, str] = {canon: style for canon, style, _aliases in INSTRUMENT_ROWS}
for _alias, _style, _by_jurisdiction in AMBIGUOUS_ROWS:
    for _jurisdiction, _canon in _by_jurisdiction:
        MARKER_STYLE.setdefault(_canon, _style)
    MARKER_STYLE[_alias + UNRESOLVED_JURISDICTION] = _style

_ALIAS_TO_CANON: dict[str, str] = {
    alias: canon for canon, _style, aliases in INSTRUMENT_ROWS for alias in aliases
}
_AMBIGUOUS: dict[str, dict[str, str]] = {
    alias: dict(by_jurisdiction) for alias, _style, by_jurisdiction in AMBIGUOUS_ROWS
}
ALIAS_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:"
    + "|".join(re.escape(a) for a in sorted([*_ALIAS_TO_CANON, *_AMBIGUOUS], key=len, reverse=True))
    + r")(?![A-Za-z0-9]|-[A-Za-z0-9])"
)
_JURISDICTION_RE = re.compile(
    r"\b(" + "|".join(sorted(JURISDICTION_WORDS, key=len, reverse=True)) + r")\b", re.IGNORECASE
)

# Citation grammar: marker, then ITEM (SEP ITEM-or-bare-subdivision)*.
_SUB = r"\((?:[0-9]{1,3}|[a-z]{1,4}|[A-Z])\)"
_NUM = r"\d{1,4}(?:-?[A-Z]{1,2}(?![a-z])|[a-z]{1,2}(?![a-z]))?(?:\.\d{1,4}[A-Z]{0,2})*(?![0-9])"
_ITEM = _NUM + "(?:" + _SUB + ")*"
_SEP = r"(?:\s*,\s*(?:and\s+|or\s+)?|\s+(?:and|or|to|through)\s+|\s*[-–]\s*|\s*[&/]\s*)"
_UNIT = r"(?![\s–-]*(?:hours?|days?|weeks?|months?|years?|minutes?|%|per\s?cent|percent)(?![A-Za-z]))"
_NOT_YEAR = r"(?!(?:19|20)\d\d(?![.\d]))"
CITE_RE = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?P<marker>Articles|Article|Arts\.|Arts|Art\.|Art|ss\.|s\.|Sections|Section|sections|section|§§|§)"
    r"\s?(?P<body>" + _ITEM + _UNIT
    + "(?:" + _SEP + _NOT_YEAR + "(?:" + _ITEM + "|(?:" + _SUB + ")+)" + _UNIT + ")*)"
)
_BODY_TOKEN_RE = re.compile(
    "(?P<item>" + _NUM + ")(?P<subs>(?:" + _SUB + ")*)"
    "|(?P<bare>(?:" + _SUB + r")+)|(?P<range>\bto\b|\bthrough\b|[-–])"
)
_EXPLICIT_ONLY_MARKERS = frozenset(("Sections", "Section", "sections", "section", "§§", "§"))

# Explicit adjacency: "GDPR Art.", "PIPEDA (s.", "the GDPR's Article", "Article 33 of the GDPR",
# "Art 26 (PDPL)". A bracket-lead postfix alias counts only when the bracket closes right after
# the alias: in "section 3.9 (MiCA Article 35(1))" the bracket opens a SEPARATE citation.
_PREFIX_TAIL_RE = re.compile(r"(?:'s)?\s*[,:]?\s*\(?\s*")
_POSTFIX_LEAD_RE = re.compile(r"\s*(?:of\s+(?:the\s+)?|(?P<paren>\(\s*))?")
_POSTFIX_CLOSE_RE = re.compile(r"\s*\)")
_ANAPHOR_RE = re.compile(r"\b(?:its|whose|their)\s+$")
_OF_THIS_RE = re.compile(r"\s*of\s+(?:this|that|such|said)\s+[A-Z]?[a-z]+")
_OF_OTHER_RE = re.compile(r"\s*of\s+(?:the\s+)?[A-Z]")
_POST_INSTRUMENT_RE = re.compile(
    r"\s+(?:Regulation|Directive|Decision|Decree|Act|Law|Code|Statute|Convention|Ordinance)\b"
)
# Inference refusal: an unaliased acronym or letter/slash-bearing identifier
# DIRECTLY before the marker, or a law word (optionally followed by a number,
# and optionally through "(") before it. A hit POISONS the rest of the line:
# an unaliased instrument is being cited here, so the line's later inferred
# tiers would misattribute. _ANAPHOR_RE refuses per-citation only.
_FOREIGN_PREFIX_RE = re.compile(
    r"(?:\b(?:[A-Z][A-Za-z]*[A-Z][\w./-]*|(?=[\w./-]*[A-Za-z/])[\w./-]*\d[\w./-]*)\s+"
    r"|\b(?:Ley|Code|Act|Law|Stat\.|Regulations?|Directive|Rules?|Decree|Norm|Standard|"
    r"Specification|Policy|Procedure|Guidelines?|Convention|Constitution|Ordinance|Regs?\.)"
    r"(?:\s+(?:No\.?\s*)?\d[\w./()-]*)?\s*[,:]?\s*\(?\s*)$"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
TITLE_RE = re.compile(r"^\*\*Document Title:\*\*\s*(.+?)\s*\\?$", re.M)


@dataclass(frozen=True)
class Citation:
    """One provision citation, or one uncited-phrase candidate, on one line."""

    path: str
    line: int
    col: int
    instrument: "str | None"
    section: str
    pinpoint: str
    tier: str
    text: str

    @property
    def key(self) -> "str | None":
        if self.instrument is None:
            return None
        return provision_key(self.instrument, self.section)


def provision_key(instrument: str, section: str) -> str:
    """Display key, e.g. ``PIPEDA s. 10.1`` or ``GDPR Art. 33``."""
    return " ".join((instrument, MARKER_STYLE.get(instrument, "s."), section))


def _path_jurisdiction(rel: str) -> "str | None":
    for token in re.split(r"[/_.-]+", rel.lower()):
        if token in JURISDICTION_WORDS:
            return JURISDICTION_WORDS[token]
    return None


def resolve_alias(alias: str, line: str, pos: int, rel: str) -> str:
    """Canonical instrument for the alias occurrence at ``pos`` on ``line``."""
    if alias in _ALIAS_TO_CANON:
        return _ALIAS_TO_CANON[alias]
    by_jurisdiction = _AMBIGUOUS[alias]
    words = _JURISDICTION_RE.findall(line[max(0, pos - JURISDICTION_WINDOW):pos])
    nearby = JURISDICTION_WORDS[words[-1].lower()] if words else None
    for jurisdiction in (nearby, _path_jurisdiction(rel)):
        if jurisdiction in by_jurisdiction:
            return by_jurisdiction[jurisdiction]
    return alias + UNRESOLVED_JURISDICTION


def aliases_in(line: str, rel: str, start: int = 0, end: "int | None" = None) -> list[str]:
    """Resolved instruments mentioned in ``line[start:end]``, in order."""
    stop = len(line) if end is None else end
    return [resolve_alias(m.group(0), line, m.start(), rel) for m in ALIAS_RE.finditer(line, start, stop)]


def _single(instruments: list[str]) -> "str | None":
    return instruments[0] if len(set(instruments)) == 1 else None


def expand_body(body: str) -> list[tuple[str, str]]:
    """``(section, pinpoint)`` pairs for a citation body such as ``10.1(2) and (6)``."""
    out: list[tuple[str, str]] = []
    base: "str | None" = None
    pending_range = False
    for tok in _BODY_TOKEN_RE.finditer(body):
        if tok.group("range"):
            pending_range = base is not None
            continue
        if tok.group("bare"):
            if base is not None:
                out.append((base, base + tok.group("bare")))
            pending_range = False
            continue
        num, subs = tok.group("item"), tok.group("subs") or ""
        if pending_range and base is not None and base.isdigit() and num.isdigit():
            lo, hi = int(base), int(num)
            if 0 < hi - lo <= MAX_RANGE_SPAN:
                out.extend((str(n), base + " to " + num) for n in range(lo + 1, hi))
        out.append((num, num + subs))
        base = num
        pending_range = False
    return out


def _snippet(line: str, start: int, end: int) -> str:
    lo, hi = max(0, start - 70), min(len(line), end + 90)
    return ("..." if lo else "") + line[lo:hi].strip() + ("..." if hi < len(line) else "")


def _context(stack: list, doc_instrument: "str | None", *, body: bool = True) -> "tuple[str | None, str]":
    """Instrument and tier from the heading chain, section body, or Document Title.

    The innermost heading wins outright (it governs its own body); the
    innermost section body is used only where no enclosing heading names a
    DIFFERENT instrument, since that conflict is a misattribution either way
    it is guessed, so it is refused.
    """
    body_instrument = stack[-1][2] if body else None
    if stack[-1][1]:
        return stack[-1][1], "heading"
    for _level, heading_instrument, _body in reversed(stack[:-1]):
        if heading_instrument:
            if body_instrument and body_instrument != heading_instrument:
                return None, UNRESOLVED
            return heading_instrument, "heading"
    if body_instrument:
        return body_instrument, "section"
    if doc_instrument:
        return doc_instrument, "document"
    return None, UNRESOLVED


def _resolve_citation(
    m: "re.Match[str]", line: str, rel: str, poisoned: bool = False
) -> "tuple[str | None, str, bool]":
    """Explicit or line-tier resolution: ``(instrument, tier, foreign prefix?)``.

    ``_NEEDS_CONTEXT`` defers to the heading chain. ``poisoned`` (a refused
    foreign-prefix citation earlier on the line) blocks the inferred tiers.
    """
    pre, post = line[:m.start()], line[m.end():]
    pre_alias = None
    for a in ALIAS_RE.finditer(pre):
        if _PREFIX_TAIL_RE.fullmatch(pre, a.end()):
            pre_alias = a
    if pre_alias:
        return resolve_alias(pre_alias.group(0), line, pre_alias.start(), rel), "explicit", False
    lead = _POSTFIX_LEAD_RE.match(post)
    post_alias = ALIAS_RE.match(post, lead.end())
    if post_alias and (not lead.group("paren") or _POSTFIX_CLOSE_RE.match(post, post_alias.end())):
        return resolve_alias(post_alias.group(0), line, m.end() + post_alias.start(), rel), "explicit", False
    foreign = bool(_FOREIGN_PREFIX_RE.search(pre))
    if foreign or _ANAPHOR_RE.search(pre) or _OF_THIS_RE.match(post) or _OF_OTHER_RE.match(post) \
            or _POST_INSTRUMENT_RE.match(post):
        return None, UNRESOLVED, foreign
    if poisoned:
        return None, UNRESOLVED, False
    earlier = aliases_in(line, rel, 0, m.start())
    if earlier:
        if _single(earlier) is None:
            return None, UNRESOLVED, False
        return earlier[-1], "line", False
    return None, _NEEDS_CONTEXT, False


def scan_text(rel: str, text: str) -> list[Citation]:
    """Every citation and uncited-phrase candidate in ``text``; ``rel`` is its display path."""
    title = TITLE_RE.search(text)
    doc_instrument = _single(aliases_in(title.group(1), rel)) if title else None
    # Heading stack entries: [level, instrument the heading names, last body mention].
    stack: list = [[0, None, None]]
    out: list[Citation] = []
    for lineno, line in iter_non_code_lines(text):
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            while stack[-1][0] >= level:
                stack.pop()
            stack.append([level, _single(aliases_in(heading.group(2), rel)), None])
        resolved_here = False
        poisoned = False
        for m in CITE_RE.finditer(line):
            instrument, tier, foreign = _resolve_citation(m, line, rel, poisoned)
            poisoned = poisoned or foreign
            if tier != "explicit" and m.group("marker") in _EXPLICIT_ONLY_MARKERS:
                continue
            if tier == _NEEDS_CONTEXT:
                instrument, tier = _context(stack[:-1] if heading else stack, doc_instrument)
            resolved_here = resolved_here or instrument is not None
            snippet = _snippet(line, m.start(), m.end())
            for section, pinpoint in expand_body(m.group("body")):
                out.append(Citation(rel, lineno, m.start(), instrument, section, pinpoint, tier, snippet))
        if not heading and not resolved_here:
            for instrument, section, pattern in SIGNATURE_PHRASE_ROWS:
                hit = re.search(pattern, line, re.IGNORECASE)
                if not hit:
                    continue
                before = aliases_in(line, rel, 0, hit.start())
                after = aliases_in(line, rel, hit.end())
                if before:
                    named = before[-1]
                elif after:
                    named = after[0]
                else:
                    named = _context(stack, doc_instrument, body=False)[0]
                if named == instrument:
                    out.append(Citation(rel, lineno, hit.start(), instrument, section, "(uncited)",
                                        PHRASE, _snippet(line, hit.start(), hit.end())))
        if not heading:
            mentioned = aliases_in(line, rel)
            if mentioned:
                stack[-1][2] = mentioned[-1]
    return out


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def corpus_files(roots) -> list[Path]:
    """The ``.md`` files under repo-relative ``roots``, generated artefacts excluded."""
    return [
        f for f in iter_scan_roots_markdown(roots, repo_root=REPO_ROOT)
        if display_path(f) not in EXCLUDED_FILES
    ]


def scan_files(files) -> list[Citation]:
    out: list[Citation] = []
    for f in files:
        text = read_text_safe(f)
        if text is not None:
            out.extend(scan_text(display_path(f), text))
    return out


def group_by_key(citations, *, tiers=TIERS, phrases: bool = True) -> dict[str, list[Citation]]:
    """Resolved citations (and, optionally, phrase candidates) grouped by provision key."""
    allowed = set(tiers) | (set((PHRASE,)) if phrases else set())
    grouped: dict[str, list[Citation]] = dict()
    for c in citations:
        if c.key is not None and c.tier in allowed:
            grouped.setdefault(c.key, []).append(c)
    return grouped


def tiers_up_to(name: str) -> tuple[str, ...]:
    """The tiers from ``explicit`` down to ``name`` inclusive (the --min-tier value)."""
    return TIERS[: TIERS.index(name) + 1]


def parse_key(spec: str) -> "str | None":
    """Normalize a typed provision (``PIPEDA s.10.1(3)``) to its key; None if no instrument."""
    for c in scan_text("<key>", spec):
        if c.tier == "explicit":
            return c.key
    return None


def parse_key_args(specs) -> list[str]:
    """Normalize each --key / --provision value; exit 2 on one naming no instrument."""
    keys: list[str] = []
    for spec in specs:
        key = parse_key(spec)
        if key is None:
            print(
                f"ERROR: {spec!r}: name the instrument and the section, for example "
                f"'PIPEDA s. 10.1' or 'GDPR Art. 33' (a bare 'Article 12(5)' names no instrument).",
                file=sys.stderr,
            )
            raise SystemExit(2)
        if UNRESOLVED_JURISDICTION in key:
            print(
                f"NOTE: {spec!r} reads as {key!r}; prefix the jurisdiction "
                f"(for example 'Singapore PDPA s. 26D') to match resolved citations.",
                file=sys.stderr,
            )
        keys.append(key)
    return keys


def unique_rows(citations) -> list[Citation]:
    """One row per (path, line, pinpoint, tier), in path and line order."""
    seen: set = set()
    rows: list[Citation] = []
    for c in sorted(citations, key=lambda c: (c.path, c.line, c.col)):
        ident = (c.path, c.line, c.pinpoint, c.tier)
        if ident not in seen:
            seen.add(ident)
            rows.append(c)
    return rows


def key_header(key: str, rows: list[Citation]) -> str:
    phrases = sum(1 for c in rows if c.tier == PHRASE)
    surfaces = len(set(c.path for c in rows))
    return (f"## {key}  ({len(rows) - phrases} citation(s), {phrases} uncited-phrase "
            f"candidate(s), {surfaces} surface(s))")


def format_row(c: Citation) -> str:
    return f"    {c.path}:{c.line}  {c.pinpoint}  [{c.tier}]  {c.text}"
