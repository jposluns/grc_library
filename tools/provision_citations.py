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
     and parenthesised subdivisions (including digit-letter and roman ones,
     ``(6a)``, ``(II)``), lists (including slashed lists, ``Art 5/6/12``)
     and ranges: ``s. 10.1(2) and (6)``, ``Arts. 33 to 34``,
     ``Arts. 44–49``, ``ss. 7 to 9, 11``. A bare parenthesised continuation
     (``and (6)``) attaches to the preceding section, replacing the deepest
     subdivision(s) of the preceding pinpoint, so ``Article 53(1)(a) and
     (b)`` reads as 53(1)(a) and 53(1)(b), not 53(b). A hyphenated pair
     that does not ascend is ONE branch-numbered section (``PIPA
     Art. 24-2``, ``s. 6-1-1306``), not a range. A numeric range spanning
     at most ``MAX_RANGE_SPAN`` sections is expanded; each interior
     section carries the range as its pinpoint (``25 to 39``). A
     continuation number DIRECTLY followed by a unit or magnitude word
     (``and 72 hours``, ``and 72-hour``, ``and 1.5 days``, ``and 20%``,
     ``and 20 million``), shaped as a year or as a canonical duration
     shorthand (``and 24h``, ``and 48h``, ``and 72h``), or opening a
     thousands-separated quantity (``and 1,000 users``) is not absorbed;
     the unit guard sees only the token straight after the number, so a
     unit one word later (``or 2 further months``) is still absorbed, and
     a non-canonical shorthand (``and 36h``) is too (both stated, not
     hidden; no corpus hit today).
  2. The KEY is section-level: ``PIPEDA s. 10.1(3)`` and ``PIPEDA s. 10.1(6)``
     both key to ``PIPEDA s. 10.1``; the pinpoint is kept for display.
  3. The INSTRUMENT is resolved in this order, and the tier is recorded:
       explicit  an alias directly before the marker (``GDPR Art. 33``,
                 ``PIPEDA (s. 10.1(2)``; this wins over an alias after the
                 citation) or directly after the citation (``Article 33 of
                 the GDPR``; a bracketed alias, ``Art 26 (PDPL)``, counts
                 only when the bracket closes right after the alias, so
                 ``section 3.9 (MiCA Article 35(1))`` never keys the outer
                 citation to MiCA). Aliases conjoined directly before the
                 marker by ``/``, ``&``, ``and`` or ``or`` (``GDPR / UK
                 GDPR Article 21``) cite the provision under EACH conjoined
                 instrument whose marker family matches; a comma chain
                 (``UK GDPR, LGPD Art 37``) is a framework enumeration and
                 never extends the adjacency. An alias-led bracket whose
                 body names another alias before it closes (``DORA (Art
                 68(7), citing DORA Arts 11-12)``) is a gloss over a mixed
                 parenthetical, so the lead does NOT count as explicit and
                 the citation falls to the inferred tiers. An adjacent
                 ambiguous alias counts only when its jurisdiction resolves
                 (rule 4): one refused by its context, or one whose
                 jurisdiction never resolves (``the section 1798.155 CPPA
                 administrative fine``: the California agency, not Canada's
                 Bill C-27), makes the citation unresolved, never explicit;
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
     At EVERY tier the resolution is then checked against the MARKER
     FAMILY: an ``Art``-family citation resolving to an ``s.``-style
     instrument (or the reverse) is refused, because the mismatch signals
     that a DIFFERENT instrument is being cited (``CCPA Article 10`` is an
     article of the 11 CCR CCPA Regulations, outside the alias table, not
     Cal. Civ. Code s. 10; Thailand's ``s. 24`` under a GDPR mention is
     the Thai PDPA's, not GDPR Art. 24).
     ``Section`` and ``§`` citations are indexed only at the explicit tier:
     a bare ``Section 4.2`` or ``§6.3`` is this corpus's internal
     cross-reference form, not a statute citation. Inference is REFUSED,
     and the citation left unresolved, where the marker directly follows an
     unaliased acronym or identifier, including one followed by a year and
     a slash- or dot-bearing one separated by a comma (``CCR s. 7001``,
     ``RTS 2025/1140 Arts 2``, ``DUAA 2025 s.80``, ``Regulation (EU)
     2025/1140, Article 4``; a closing bracket or a sentence period blocks
     the comma shape, so ``the EU AI Act (Regulation (EU) 2024/1689),
     Article 50`` still resolves), a law word optionally followed by an
     ``(EU)``-style qualifier and a number (``Ley Art 33``, ``the Privacy
     Act (s. 3)``, ``Decree 356 Art. 20``) or a possessive or relative
     reference to another instrument (``its Articles 46 and 48``,
     ``whose Article 11``), or the citation is followed by ``of this Law``,
     ``of that Regulation`` or ``of <Name>``, or directly by an instrument
     word (``Article 29(7) Regulation (EU) 2018/1725``): inference there
     would attach the citation to whichever aliased instrument happened to
     be mentioned nearby.
  4. Ambiguous short names (``PDPA``, ``PDPL``, ``CPPA``, ``PIPA``,
     ``AI Act``) resolve by the last jurisdiction word within
     ``JURISDICTION_WINDOW`` characters before the alias (a jurisdiction
     word inside another alias mention, the ``EU`` of ``EU GDPR``, does
     not count), then by a jurisdiction token in the document path, else
     to ``<alias> (jurisdiction unresolved)`` — a key that can carry only
     INFERRED-tier citations (rule 3 refuses it at the explicit tier), so
     its rows always print as unverified candidates. A jurisdiction context the
     alias's table row does not list REFUSES the mention outright: near
     ``California``, ``CPPA`` is the California Privacy Protection Agency
     (an authority, not Canada's Bill C-27 statute), so the token names no
     instrument and a citation adjacent to it is unresolved. An alias used
     as an adjectival compound (``GDPR-style``, ``GDPR-Article-26-style``)
     is not a mention.
  5. SIGNATURE PHRASES: a small seed table of phrases that restate a
     provision WITHOUT citing it (before #2649 most PIPEDA s. 10.1 surfaces
     carried no section number at all). A hit is reported with tier
     ``phrase`` as an uncited-restatement CANDIDATE, only on a non-heading
     line that carries no resolved citation, and only when the phrase's
     instrument context is the key's instrument: the nearest alias before
     the phrase on the line, else the first after it, else the heading
     chain, else the Document Title (the weaker section-body tier is not
     used for phrases).

The explicit tier is trusted; every other citation tier is an INFERENCE,
and the two tools list inferred-tier rows under ``CANDIDATE_LABEL``,
separated from the explicit rows. Residue is stated in the two tools'
docstrings.

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
# The label both tools print above inferred-tier and uncited-phrase rows: those
# rows are candidates whose instrument a reviewer must confirm, not siblings.
CANDIDATE_LABEL = "unverified candidates (inferred instrument)"
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
_SUB = r"\((?:[0-9]{1,3}[a-z]{0,2}|[a-z]{1,4}|[A-Z]|[IVX]{2,5})\)"
_NUM = r"\d{1,4}(?:-?[A-Z]{1,2}(?![a-z])|[a-z]{1,2}(?![a-z]))?(?:\.\d{1,4}[A-Z]{0,2})*(?![0-9])"
_ITEM = _NUM + "(?:" + _SUB + ")*"
_SEP = r"(?:\s*,\s*(?:and\s+|or\s+)?|\s+(?:and|or|to|through)\s+|\s*[-–]\s*|\s*[&/]\s*)"
# The decimal alternative stops _NUM backtracking out of "1.5" to absorb the
# "1" of "and 1.5 days" as a section once the unit rejects the full number.
_UNIT = (
    r"(?!(?:\.\d+)?[\s–-]*(?:hours?|hrs?|h|days?|weeks?|wks?|months?|years?|yrs?|"
    r"minutes?|mins?|millions?|billions?|thousands?|%|per\s?cent|percent)(?![A-Za-z]))"
)
# A comma directly binding two digit groups whose right group is exactly three
# digits is a thousands separator ("1,000 users"), not a list; and the bare
# canonical duration shorthands 24h/48h/72h are quantities, not sections (a
# letter-suffixed article such as "Art. 5h" stays parseable; a non-canonical
# shorthand, "36h", is stated residue).
_NOT_THOUSANDS = r"(?!,\d{3}(?![0-9]))"
_NOT_SHORTHAND = r"(?!(?:24|48|72)h(?![A-Za-z0-9]))"
_NOT_YEAR = r"(?!(?:19|20)\d\d(?![.\d]))"
CITE_RE = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?P<marker>Articles|Article|Arts\.|Arts|Art\.|Art|ss\.|s\.|Sections|Section|sections|section|§§|§)"
    r"\s?(?P<body>" + _ITEM + _NOT_THOUSANDS + _UNIT
    + "(?:" + _SEP + _NOT_YEAR + _NOT_SHORTHAND
    + "(?:" + _ITEM + "|(?:" + _SUB + ")+)" + _NOT_THOUSANDS + _UNIT + ")*)"
)
_BODY_TOKEN_RE = re.compile(
    "(?P<item>" + _NUM + ")(?P<subs>(?:" + _SUB + ")*)"
    "|(?P<bare>(?:" + _SUB + r")+)|(?P<range>\bto\b|\bthrough\b|[-–])"
)
_SUB_SPLIT_RE = re.compile(r"\([^()]*\)")
_EXPLICIT_ONLY_MARKERS = frozenset(("Sections", "Section", "sections", "section", "§§", "§"))

# Explicit adjacency: "GDPR Art.", "PIPEDA (s.", "the GDPR's Article", "Article 33 of the GDPR",
# "Art 26 (PDPL)". A bracket-lead postfix alias counts only when the bracket closes right after
# the alias: in "section 3.9 (MiCA Article 35(1))" the bracket opens a SEPARATE citation.
_PREFIX_TAIL_RE = re.compile(r"(?:'s)?\s*[,:]?\s*\(?\s*")
# Conjunctions that extend an explicit prefix to every conjoined alias
# ("GDPR / UK GDPR Article 21", "GDPR and UK GDPR Article 28"). A comma is
# NOT one: "UK GDPR, LGPD Art 37" enumerates frameworks, and chaining it
# would misattribute LGPD's article to UK GDPR.
_CONJ_RE = re.compile(r"\s*(?:[/&]|\band\b|\bor\b)\s*")
_POSTFIX_LEAD_RE = re.compile(r"\s*(?:of\s+(?:the\s+)?|(?P<paren>\(\s*))?")
_POSTFIX_CLOSE_RE = re.compile(r"\s*\)")
_ANAPHOR_RE = re.compile(r"\b(?:its|whose|their)\s+$")
_OF_THIS_RE = re.compile(r"\s*of\s+(?:this|that|such|said)\s+[A-Z]?[a-z]+")
_OF_OTHER_RE = re.compile(r"\s*of\s+(?:the\s+)?[A-Z]")
_POST_INSTRUMENT_RE = re.compile(
    r"\s+(?:Regulation|Directive|Decision|Decree|Act|Law|Code|Statute|Convention|Ordinance)\b"
)
# Inference refusal, three branches, each anchored at the marker. (1) An
# unaliased acronym or letter/slash-bearing identifier directly before the
# marker, optionally with a year between them ("DUAA 2025 s.80"). (2) A slash-
# or dot-bearing numeric identifier separated from the marker by a comma
# ("2025/1140, Article 4"; balanced parens are part of the identifier,
# "125(I)/2018,", but a bare closing bracket or a sentence period ends it, so
# "(Regulation (EU) 2024/1689), Article 50" is NOT refused when the bracketed
# name is an alias resolving by line context). (3) A law word, optionally with
# an "(EU)"-style qualifier and a number, through ",", ":" or "(". A hit
# POISONS the rest of the line: an unaliased instrument is being cited here,
# so the line's later inferred tiers would misattribute. _ANAPHOR_RE refuses
# per-citation only.
_FOREIGN_PREFIX_RE = re.compile(
    r"(?:\b(?:[A-Z][A-Za-z]*[A-Z][\w./-]*|(?=[\w./-]*[A-Za-z/])[\w./-]*\d[\w./-]*)"
    r"(?:\s+(?:19|20)\d\d)?\s+"
    r"|\b(?=[\w./()-]*[/.])(?=[\w./()-]*\d)[\w./-]+(?:\([A-Za-z0-9]+\)[\w./-]*)*\s*,\s*"
    r"|\b(?:Ley|Code|Act|Law|Stat\.|Regulations?|Directive|Rules?|Decree|Norm|Standard|"
    r"Specification|Policy|Procedure|Guidelines?|Convention|Constitution|Ordinance|Regs?\.)"
    r"(?:\s+\([A-Z]{2,3}\))?(?:\s+(?:No\.?\s*)?\d[\w./-]*)?\s*[,:]?\s*\(?\s*)$"
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


def _marker_family(marker: str) -> str:
    """``Art.`` for the Article-marker family, ``s.`` for s./ss./Section/section/§."""
    return "Art." if marker.startswith("Art") else "s."


def _path_jurisdiction(rel: str) -> "str | None":
    for token in re.split(r"[/_.-]+", rel.lower()):
        if token in JURISDICTION_WORDS:
            return JURISDICTION_WORDS[token]
    return None


def resolve_alias(alias: str, line: str, pos: int, rel: str) -> "str | None":
    """Canonical instrument for the alias occurrence at ``pos`` on ``line``.

    None where the jurisdiction context contradicts the alias's table row
    (near ``California``, ``CPPA`` is the state agency, not Canada's Bill
    C-27): the mention then names no instrument at all. A jurisdiction word
    inside another alias mention (the ``EU`` of ``EU GDPR``) describes that
    alias, not this one, and is not context.
    """
    if alias in _ALIAS_TO_CANON:
        return _ALIAS_TO_CANON[alias]
    by_jurisdiction = _AMBIGUOUS[alias]
    lo = max(0, pos - JURISDICTION_WINDOW)
    spans = [a.span() for a in ALIAS_RE.finditer(line)]
    words = [
        w.group(1) for w in _JURISDICTION_RE.finditer(line[lo:pos])
        if not any(s <= lo + w.start() and lo + w.end() <= e for s, e in spans)
    ]
    nearby = JURISDICTION_WORDS[words[-1].lower()] if words else None
    for jurisdiction in (nearby, _path_jurisdiction(rel)):
        if jurisdiction is None:
            continue
        return by_jurisdiction.get(jurisdiction)
    return alias + UNRESOLVED_JURISDICTION


def aliases_in(line: str, rel: str, start: int = 0, end: "int | None" = None) -> list[str]:
    """Resolved instruments mentioned in ``line[start:end]``, in order.

    A refused mention (an ambiguous alias contradicted by its jurisdiction
    context) appears as None, so ``_single`` and the line tier treat it as
    a second, unknown instrument rather than skipping it.
    """
    stop = len(line) if end is None else end
    return [resolve_alias(m.group(0), line, m.start(), rel) for m in ALIAS_RE.finditer(line, start, stop)]


def _single(instruments: list[str]) -> "str | None":
    return instruments[0] if len(set(instruments)) == 1 else None


def expand_body(body: str) -> list[tuple[str, str]]:
    """``(section, pinpoint)`` pairs for a citation body such as ``10.1(2) and (6)``."""
    out: list[tuple[str, str]] = []
    base: "str | None" = None
    base_subs: list[str] = []
    pending_range = False
    hyphen_range = False
    branch = False
    for tok in _BODY_TOKEN_RE.finditer(body):
        if tok.group("range"):
            pending_range = base is not None
            hyphen_range = tok.group("range") in ("-", "–")
            continue
        if tok.group("bare"):
            if base is not None:
                # "53(1)(a) and (b)" means 53(1)(b): the continuation replaces the
                # deepest subdivision(s) of the previous pinpoint, keeping the parent.
                subs = _SUB_SPLIT_RE.findall(tok.group("bare"))
                kept = base_subs[: -len(subs)] if len(subs) < len(base_subs) else []
                base_subs = kept + subs
                out.append((base, base + "".join(base_subs)))
            pending_range = False
            continue
        num, subs = tok.group("item"), tok.group("subs") or ""
        if pending_range and base is not None and num.isdigit():
            if hyphen_range and (branch or (base.isdigit() and int(num) <= int(base))):
                # A hyphen pair that does not ascend is a branch-numbered section
                # (PIPA Art. 24-2, Colorado s. 6-1-1306), not a range: fold it into
                # the preceding number (chained folds keep folding).
                out.pop()
                num = base + "-" + num
                out.append((num, num + subs))
                base = num
                base_subs = _SUB_SPLIT_RE.findall(subs)
                branch = True
                pending_range = False
                continue
            if base.isdigit():
                lo, hi = int(base), int(num)
                if 0 < hi - lo <= MAX_RANGE_SPAN:
                    out.extend((str(n), base + " to " + num) for n in range(lo + 1, hi))
        out.append((num, num + subs))
        base = num
        base_subs = _SUB_SPLIT_RE.findall(subs)
        branch = False
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


def _known(instrument: "str | None") -> bool:
    """True for a fully resolved instrument: the EXPLICIT tier requires one.

    A refused mention (None) or an ambiguous alias whose jurisdiction never
    resolved (``PDPA (jurisdiction unresolved)``) is not a known instrument,
    so adjacency to it cannot be trusted; such keys still surface at the
    inferred tiers, as unverified candidates.
    """
    return instrument is not None and UNRESOLVED_JURISDICTION not in instrument


def _resolve_citation(
    m: "re.Match[str]", line: str, rel: str, poisoned: bool = False
) -> "tuple[list[str], str, bool]":
    """Explicit or line-tier resolution: ``(instruments, tier, foreign prefix?)``.

    ``instruments`` usually holds one instrument; a conjoined explicit prefix
    (``GDPR / UK GDPR Article 21``) holds one per conjoined alias, and an
    empty list is a refusal. ``_NEEDS_CONTEXT`` defers to the heading chain.
    ``poisoned`` (a refused foreign-prefix citation earlier on the line)
    blocks the inferred tiers.
    """
    pre, post = line[:m.start()], line[m.end():]
    pre_alias = None
    for a in ALIAS_RE.finditer(pre):
        if _PREFIX_TAIL_RE.fullmatch(pre, a.end()):
            pre_alias = a
    if pre_alias:
        close = post.find(")")
        gloss = "(" in pre[pre_alias.end():] and bool(
            ALIAS_RE.search(post if close < 0 else post[:close]))
        # An alias-led bracket that re-names an instrument before it closes
        # ("DORA (Art 68(7), citing DORA Arts 11-12)") is a gloss over a
        # mixed parenthetical, not a citation adjacency: fall through to the
        # inferred tiers instead of trusting it as explicit.
        if not gloss:
            chain = [pre_alias]
            while True:
                prev = None
                for a in ALIAS_RE.finditer(pre, 0, chain[0].start()):
                    if _CONJ_RE.fullmatch(pre, a.end(), chain[0].start()):
                        prev = a
                if prev is None:
                    break
                chain.insert(0, prev)
            resolved = [resolve_alias(a.group(0), line, a.start(), rel) for a in chain]
            if not _known(resolved[-1]):
                # The adjacent token pattern-matches an alias but names no
                # single known instrument: its jurisdiction context contradicts
                # the table, or never resolves at all (the California CPPA
                # agency next to "s. 1798.155" reads exactly like a statute
                # citation). The record is unresolved, never explicit.
                return [], UNRESOLVED, False
            instruments: list[str] = []
            for r in resolved:
                if _known(r) and r not in instruments:
                    instruments.append(r)
            return instruments, "explicit", False
    lead = _POSTFIX_LEAD_RE.match(post)
    post_alias = ALIAS_RE.match(post, lead.end())
    if post_alias and (not lead.group("paren") or _POSTFIX_CLOSE_RE.match(post, post_alias.end())):
        instrument = resolve_alias(post_alias.group(0), line, m.end() + post_alias.start(), rel)
        if not _known(instrument):
            return [], UNRESOLVED, False
        return [instrument], "explicit", False
    foreign = bool(_FOREIGN_PREFIX_RE.search(pre))
    if foreign or _ANAPHOR_RE.search(pre) or _OF_THIS_RE.match(post) or _OF_OTHER_RE.match(post) \
            or _POST_INSTRUMENT_RE.match(post):
        return [], UNRESOLVED, foreign
    if poisoned:
        return [], UNRESOLVED, False
    earlier = aliases_in(line, rel, 0, m.start())
    if earlier:
        single = _single(earlier)
        if single is None:
            return [], UNRESOLVED, False
        return [single], "line", False
    return [], _NEEDS_CONTEXT, False


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
            instruments, tier, foreign = _resolve_citation(m, line, rel, poisoned)
            poisoned = poisoned or foreign
            if tier != "explicit" and m.group("marker") in _EXPLICIT_ONLY_MARKERS:
                continue
            if tier == _NEEDS_CONTEXT:
                instrument, tier = _context(stack[:-1] if heading else stack, doc_instrument)
                instruments = [instrument] if instrument is not None else []
            family = _marker_family(m.group("marker"))
            if instruments and MARKER_STYLE.get(instruments[-1]) != family:
                # Marker-family guard: an Art-marker citation cannot belong to an
                # s.-style statute (or the reverse) — the resolved instrument is the
                # wrong one ("CCPA Article 10" is an 11 CCR regulation article), so
                # refuse rather than misattribute, at every tier.
                instruments, tier = [], UNRESOLVED
            elif len(instruments) > 1:
                # A conjoined prefix member of the other marker family ("SOX and
                # GDPR Articles 5(2)") is an enumeration entry alongside the
                # citation, not a co-citation of this provision: drop it.
                instruments = [i for i in instruments if MARKER_STYLE.get(i) == family]
            resolved_here = resolved_here or bool(instruments)
            snippet = _snippet(line, m.start(), m.end())
            for section, pinpoint in expand_body(m.group("body")):
                for instrument in instruments or [None]:
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
                f"'PIPEDA s. 10.1' or 'GDPR Art. 33' (a bare 'Article 12(5)' names no "
                f"instrument, and an ambiguous short name needs its jurisdiction: "
                f"'Singapore PDPA s. 26D', not 'PDPA s. 26D').",
                file=sys.stderr,
            )
            raise SystemExit(2)
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


def split_rows(rows, trusted=("explicit",)) -> "tuple[list[Citation], list[Citation]]":
    """Partition ``rows`` into (trusted rows, unverified candidate rows).

    A row whose tier is in ``trusted`` is a sibling a reviewer can act on;
    every other row — an inferred-instrument tier outside ``trusted`` or an
    uncited-phrase hit — is a candidate to print under ``CANDIDATE_LABEL``.
    """
    return ([c for c in rows if c.tier in trusted],
            [c for c in rows if c.tier not in trusted])


def key_header(key: str, rows: list[Citation]) -> str:
    phrases = sum(1 for c in rows if c.tier == PHRASE)
    surfaces = len(set(c.path for c in rows))
    return (f"## {key}  ({len(rows) - phrases} citation(s), {phrases} uncited-phrase "
            f"candidate(s), {surfaces} surface(s))")


def format_row(c: Citation) -> str:
    return f"    {c.path}:{c.line}  {c.pinpoint}  [{c.tier}]  {c.text}"
