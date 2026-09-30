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
     section carries the range as its pinpoint (``25 to 39``), while the
     endpoints keep the pinpoints they are cited with (``25``, ``39(2)``).
     A range from a decimal section reads an integer endpoint as
     ABBREVIATED when it has the start's sub-number width and ascends
     (``HIPAA §164.400 to 414`` is 164.400 to 164.414, interior sections
     included) or as a WHOLE section when it ascends from the start's
     section within ``MAX_RANGE_SPAN`` (``s. 10.1 to 12``); an endpoint
     that reads both ways or neither (``ss. 3.1 to 5``) is recorded
     unresolved, never keyed. A continuation number DIRECTLY followed by a
     unit, magnitude or month word (``and 72 hours``, ``and 72-hour``,
     ``and 1.5 days``, ``and 20%``, ``and 20 million``, ``and 2 August
     2026``), or by one quantity adjective and a unit (``and 2 further
     months``), shaped as a year or as a canonical duration shorthand
     (``and 12h`` ... ``and 96h``), or opening a thousands-separated
     quantity (``and 1,000 users``) is not absorbed; a unit two words
     later (``or 2 more calendar months``) is still absorbed, and a
     non-canonical shorthand (``and 30h``) is too (both stated, not
     hidden; no corpus hit today). A citation-shaped body name
     (``Article 29 Working Party``, ``Art. 29 WP``) is not a citation.
  2. The KEY is section-level: ``PIPEDA s. 10.1(3)`` and ``PIPEDA s. 10.1(6)``
     both key to ``PIPEDA s. 10.1``; the pinpoint is kept for display.
  3. The INSTRUMENT is resolved in this order, and the tier is recorded:
       explicit  an alias directly before the marker (``GDPR Art. 33``,
                 ``PIPEDA (s. 10.1(2)``, ``the GDPR's Article``, ``GDPR:
                 Article``, ``Under the LGPD, Article``; this wins over a
                 bracketed alias after the citation) or directly after the
                 citation (``Article 33 of the GDPR``, ``Article 9(2),
                 point (g), of the GDPR``: a point or subparagraph
                 designation may sit between; a bracketed alias, ``Art 26
                 (PDPL)``, counts only when the bracket closes right after
                 the alias, so ``section 3.9 (MiCA Article 35(1))`` never
                 keys the outer citation to MiCA). A prefix alias does not
                 count when the text after the citation names an instrument
                 (``Unlike the GDPR, Article 12 of the Data Act``, ``GDPR,
                 Article 12 Regulation (EU) 2023/2854``, ``of that
                 Regulation``): the citation is then resolved by that tail
                 (``the GDPR, Article 12 of PIPL`` is PIPL Art. 12) or
                 refused. A postfix alias that modifies a subordinate
                 instrument (``Article 12 of the DORA RTS``, ``s. 7012 CCPA
                 Regulations``, ``Article 4 of the NIS2 Implementing
                 Regulation``) does not count either: the citation is
                 refused. Aliases conjoined directly before the marker by
                 ``/``, ``&``, ``and`` or ``or`` (``GDPR / UK GDPR Article
                 21``) cite the provision under EACH conjoined instrument
                 whose marker family matches: explicitly where the member
                 shares the adjacent alias's article numbering
                 (``SHARED_NUMBERING``: GDPR and UK GDPR), else at the line
                 tier, since ``the LGPD and GDPR Article 20`` cites GDPR
                 portability, not LGPD Art. 20; a comma chain (``UK GDPR,
                 LGPD Art 37``) is a framework enumeration and never
                 extends the adjacency. An alias-led bracket whose body
                 names an alias (the same one or another) before it closes
                 (``DORA (Art 68(7), citing DORA Arts 11-12)``) is a gloss
                 over a mixed parenthetical, so the lead does NOT count as
                 explicit, and the citation falls to the inferred tiers
                 WITHOUT that lead (in the MiCA annex, Art 68(7) resolves
                 to MiCA from the heading, not to DORA). An adjacent
                 ambiguous alias counts only when its jurisdiction resolves
                 (rule 4): one refused by its context, or one whose
                 jurisdiction never resolves (``the section 1798.155 CPPA
                 administrative fine``: the California agency, not Canada's
                 Bill C-27), makes the citation unresolved, never explicit;
       line      the nearest alias earlier on the same line (a table row,
                 or prose), only when every such alias names ONE instrument
                 and no foreign-prefix refusal precedes the citation on the
                 line (such a refusal means an instrument outside the alias
                 table is being cited there, so the line's later bare
                 citations are plausibly its, not the alias's). An alias
                 that an earlier citation on the line took as its POSTFIX
                 instrument (``Article 35 GDPR``) binds to that citation and
                 is not reused (in the EU AI annex, ``... Article 35 GDPR ...
                 Article 27(4)`` is the AI Act's, and is no longer keyed as
                 GDPR Art. 27); a prefix alias is reused (``GDPR Art. 33;
                 notify (Art. 34)``);
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
     ``of that Regulation`` or ``of <Name>`` (through a point designation
     too: ``Article 2, point (9), of Regulation (EU) 2017/1131``), or
     directly by an instrument word (``Article 29(7) Regulation (EU)
     2018/1725``): inference there would attach the citation to whichever
     aliased instrument happened to be mentioned nearby.
  4. Ambiguous short names (``PDPA``, ``PDPL``, ``CPPA``, ``PIPA``,
     ``AI Act``) resolve by the last jurisdiction word within
     ``JURISDICTION_WINDOW`` characters before the alias (a jurisdiction
     word inside another alias mention, the ``EU`` of ``EU GDPR``, does
     not count), then by a jurisdiction token in the document path, else
     to ``<alias> (jurisdiction unresolved)`` — a key that can carry only
     INFERRED-tier citations (rule 3 refuses it at the explicit tier, and a
     conjoined member of that kind is dropped, so ``AI Act / EU AI Act
     Art. 50`` keys only the EU AI Act), so its rows always print as
     unverified candidates. A jurisdiction context the
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
separated from the explicit rows. ``parse_key`` accepts every key the tools
print (``PDPA (Singapore) s. 26D``, ``HIPAA (45 CFR) s. 164.308``) as well as
an explicit citation. Residue is stated in the two tools' docstrings.

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

# Instrument sets whose article NUMBERING coincides (the UK GDPR keeps the
# GDPR's article numbers), so a conjoined prefix ("GDPR / UK GDPR Article 21")
# cites the same provision under each. Any other conjoined member names an
# instrument whose same-numbered article may be unrelated ("the LGPD and GDPR
# Article 20" cites GDPR portability, not LGPD Art. 20), so its record is an
# inference (line tier), not explicit.
SHARED_NUMBERING: tuple[frozenset[str], ...] = (frozenset(("GDPR", "UK GDPR")),)

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

# Every canonical instrument name, longest first: parse_key accepts a key
# exactly as printed, and a canonical name is not always an alias.
_CANONICAL_BY_LENGTH: list[str] = sorted(MARKER_STYLE, key=len, reverse=True)
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
# A capitalized month name makes the number a day of the month ("Art. 113 and
# 2 August 2026"), and one quantity adjective may sit between a number and its
# unit ("and 2 further months").
_MONTHS = (
    r"January|February|March|April|May|June|July|August|September|October|November|December|"
    r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec"
)
_UNIT = (
    r"(?!(?:\.\d+)?[\s–-]*(?:(?:further|more|additional|extra|calendar|business|working|clear|"
    r"consecutive)\s+)?(?:hours?|hrs?|h|days?|weeks?|wks?|months?|years?|yrs?|minutes?|mins?|"
    r"millions?|billions?|thousands?|%|per\s?cent|percent|" + _MONTHS + r")(?![A-Za-z]))"
)
# A comma directly binding two digit groups whose right group is exactly three
# digits is a thousands separator ("1,000 users"), not a list; and the bare
# canonical duration shorthands 12h/24h/36h/48h/72h/96h are quantities, not
# sections (a letter-suffixed article such as "Art. 5h" stays parseable; a
# non-canonical shorthand, "30h", is stated residue).
_NOT_THOUSANDS = r"(?!,\d{3}(?![0-9]))"
_NOT_SHORTHAND = r"(?!(?:12|24|36|48|72|96)h(?![A-Za-z0-9]))"
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
_DECIMAL_RE = re.compile(r"(\d+)\.(\d+)")
# A citation-shaped token that names a BODY, not a provision ("Article 29
# Working Party", "Art. 29 WP"): it is skipped, never indexed.
_BODY_NAME_RE = re.compile(r"\s+(?:Working\s+Party|WP)\b")

# Explicit adjacency: "GDPR Art.", "PIPEDA (s.", "the GDPR's Article", "Article 33 of the GDPR",
# "Art 26 (PDPL)". A bracket-lead postfix alias counts only when the bracket closes right after
# the alias: in "section 3.9 (MiCA Article 35(1))" the bracket opens a SEPARATE citation.
_PREFIX_TAIL_RE = re.compile(r"(?:'s)?\s*[,:]?\s*\(?\s*")
# Conjunctions that extend an explicit prefix to every conjoined alias
# ("GDPR / UK GDPR Article 21", "GDPR and UK GDPR Article 28"). A comma is
# NOT one: "UK GDPR, LGPD Art 37" enumerates frameworks, and chaining it
# would misattribute LGPD's article to UK GDPR.
_CONJ_RE = re.compile(r"\s*(?:[/&]|\band\b|\bor\b)\s*")
# A point or subparagraph designation between a citation and "of <instrument>"
# ("Article 9(2), point (g), of the GDPR") belongs to the pinpoint's wording: it
# neither blocks postfix resolution nor hides an "of <Name>" refusal.
_POINT = (
    r"(?:(?:,?\s*(?:(?:first|second|third|fourth|fifth|sixth)\s+subparagraph|points?\s+"
    r"\([a-z0-9]{1,4}\)(?:\s*(?:,|and|or|to)\s*\([a-z0-9]{1,4}\))*)){1,3}\s*,?\s+(?=of\b))?"
)
_POSTFIX_LEAD_RE = re.compile(r"\s*(?:" + _POINT + r"of\s+(?:the\s+)?|(?P<paren>\(\s*))?")
_POSTFIX_CLOSE_RE = re.compile(r"\s*\)")
_ANAPHOR_RE = re.compile(r"\b(?:its|whose|their)\s+$")
_OF_THIS_RE = re.compile(r"\s*" + _POINT + r"of\s+(?:this|that|such|said)\s+[A-Z]?[a-z]+")
_OF_OTHER_RE = re.compile(r"\s*" + _POINT + r"of\s+(?:the\s+)?[A-Z]")
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
# A postfix alias that MODIFIES a subordinate instrument ("Article 12 of the
# DORA RTS", "s. 7012 CCPA Regulations", "section 3 of the PIPEDA Breach of
# Security Safeguards Regulations") names that instrument, not the alias's, so
# the citation is refused. A singular "Regulation", "Directive", "Act" or
# "Rule" after the alias is the aliased instrument itself ("the NIS2
# Directive"; the "HIPAA Security Rule" is 45 CFR Part 164) and is not.
_SUBORDINATE_RE = re.compile(
    r"(?:'s)?(?:\s+(?:[A-Z][\w&-]*|of)){0,5}?\s+(?:RTS|ITS|Regulations|Rules|Implementing|Delegated|"
    r"Guidelines|Technical\s+Standards|Decree|Ordinance|Order)\b"
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


def _decimal_end(base: str, num: str) -> "tuple[str | None, list[str]]":
    """Endpoint and interior sections of a range that STARTS at a decimal section.

    ``HIPAA §164.400 to 414`` abbreviates ``164.414``. An integer endpoint
    reads as ABBREVIATED when it has the start's sub-number width and
    ascends from it, and as a WHOLE section (``s. 10.1 to 12``) when it
    ascends from the start's section by at most ``MAX_RANGE_SPAN``. Exactly
    one reading must hold; otherwise (``ss. 3.1 to 5``: s. 3.5, or s. 5?)
    the endpoint is doubtful and returned as None. A decimal endpoint is
    kept as written. Interior sections are listed only for a same-section
    range of one sub-number width spanning at most ``MAX_RANGE_SPAN`` steps
    (``164.401`` ... ``164.413``).
    """
    whole, sub = _DECIMAL_RE.fullmatch(base).groups()
    full = _DECIMAL_RE.fullmatch(num)
    if full:
        if full.group(1) != whole or len(full.group(2)) != len(sub):
            return num, []
        end_sub = full.group(2)
    elif num.isdigit():
        abbreviated = len(num) == len(sub) and int(num) > int(sub)
        whole_end = 0 < int(num) - int(whole) <= MAX_RANGE_SPAN
        if abbreviated == whole_end:
            return None, []
        if whole_end:
            return num, []
        end_sub = num
    else:
        return num, []
    end = whole + "." + end_sub
    lo, hi = int(sub), int(end_sub)
    if not 0 < hi - lo <= MAX_RANGE_SPAN:
        return end, []
    return end, [whole + "." + str(n).zfill(len(sub)) for n in range(lo + 1, hi)]


def expand_body(body: str) -> list[tuple[str, str, bool]]:
    """``(section, pinpoint, certain)`` triples for a citation body such as ``10.1(2) and (6)``.

    ``certain`` is False only for a doubtful range endpoint (see
    ``_decimal_end``) and a bare continuation of one: the caller records
    those as unresolved rather than keying a guessed section. A range's
    endpoints carry their own pinpoints as cited (``25``, ``39(2)``); only
    the interior sections, which the text never names, carry the range
    (``25 to 39``).
    """
    out: list[tuple[str, str, bool]] = []
    base: "str | None" = None
    base_subs: list[str] = []
    base_certain = True
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
                out.append((base, base + "".join(base_subs), base_certain))
            pending_range = False
            continue
        num, subs = tok.group("item"), tok.group("subs") or ""
        certain = True
        if pending_range and base is not None:
            if num.isdigit() and hyphen_range and (branch or (base.isdigit() and int(num) <= int(base))):
                # A hyphen pair that does not ascend is a branch-numbered section
                # (PIPA Art. 24-2, Colorado s. 6-1-1306), not a range: fold it into
                # the preceding number (chained folds keep folding).
                out.pop()
                num = base + "-" + num
                out.append((num, num + subs, base_certain))
                base = num
                base_subs = _SUB_SPLIT_RE.findall(subs)
                branch = True
                pending_range = False
                continue
            if base.isdigit() and num.isdigit():
                lo, hi = int(base), int(num)
                if 0 < hi - lo <= MAX_RANGE_SPAN:
                    out.extend((str(n), base + " to " + num, True) for n in range(lo + 1, hi))
            elif base_certain and _DECIMAL_RE.fullmatch(base):
                end, interior = _decimal_end(base, num)
                if end is None:
                    certain = False
                else:
                    out.extend((s, base + " to " + end, True) for s in interior)
                    num = end
        out.append((num, num + subs, certain))
        base = num
        base_subs = _SUB_SPLIT_RE.findall(subs)
        base_certain = certain
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


def _shares_numbering(a: str, b: str) -> bool:
    return a == b or any(a in group and b in group for group in SHARED_NUMBERING)


def _resolve_citation(
    m: "re.Match[str]", line: str, rel: str, poisoned: bool = False, claimed=frozenset()
) -> "tuple[list[tuple[str, str]], str, bool, int | None]":
    """Explicit or line-tier resolution: ``(attributions, tier, foreign prefix?, claim)``.

    ``attributions`` pairs each instrument with its record tier. It usually
    holds one pair; a conjoined explicit prefix (``GDPR / UK GDPR Article
    21``) holds one per conjoined alias (explicit where the member shares
    the adjacent alias's numbering, ``SHARED_NUMBERING``, else line tier),
    and an empty list is a refusal. ``_NEEDS_CONTEXT`` defers to the heading
    chain. ``poisoned`` (a refused foreign-prefix citation earlier on the
    line) blocks the inferred tiers. ``claimed`` holds the start of every
    alias an earlier citation on the line took as its POSTFIX instrument
    (``Article 35 GDPR``): such an alias binds to its own citation, so the
    line tier never reuses it. ``claim`` is the start of the postfix alias
    this citation takes, or None.
    """
    pre, post = line[:m.start()], line[m.end():]
    # A tail naming an instrument ("of the Data Act", "of that Regulation",
    # "Regulation (EU) 2023/2854") says whose provision this is, so an alias
    # BEFORE the citation, however adjacent, is not trusted as its instrument.
    other_tail = bool(_OF_THIS_RE.match(post) or _OF_OTHER_RE.match(post)
                      or _POST_INSTRUMENT_RE.match(post))
    excluded = set(claimed)
    pre_alias = None
    for a in ALIAS_RE.finditer(pre):
        if _PREFIX_TAIL_RE.fullmatch(pre, a.end()):
            pre_alias = a
    if pre_alias and not other_tail:
        close = post.find(")")
        gloss = "(" in pre[pre_alias.end():] and bool(
            ALIAS_RE.search(post if close < 0 else post[:close]))
        if gloss:
            # An alias-led bracket that names an alias (the same one or another)
            # before it closes ("DORA (Art 68(7), citing DORA Arts 11-12)") is a
            # gloss over a mixed parenthetical: the lead is not this citation's
            # instrument, so it is neither explicit nor reused by the line tier.
            excluded.add(pre_alias.start())
        else:
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
                return [], UNRESOLVED, False, None
            attributions: list[tuple[str, str]] = []
            for r in resolved:
                if _known(r) and r not in [i for i, _t in attributions]:
                    tier = "explicit" if _shares_numbering(r, resolved[-1]) else "line"
                    attributions.append((r, tier))
            return attributions, "explicit", False, None
    lead = _POSTFIX_LEAD_RE.match(post)
    post_alias = ALIAS_RE.match(post, lead.end())
    if post_alias and (not lead.group("paren") or _POSTFIX_CLOSE_RE.match(post, post_alias.end())):
        if _SUBORDINATE_RE.match(post, post_alias.end()):
            return [], UNRESOLVED, False, None
        instrument = resolve_alias(post_alias.group(0), line, m.end() + post_alias.start(), rel)
        if not _known(instrument):
            return [], UNRESOLVED, False, None
        return [(instrument, "explicit")], "explicit", False, m.end() + post_alias.start()
    foreign = bool(_FOREIGN_PREFIX_RE.search(pre))
    if foreign or _ANAPHOR_RE.search(pre) or other_tail:
        return [], UNRESOLVED, foreign, None
    if poisoned:
        return [], UNRESOLVED, False, None
    earlier = [resolve_alias(a.group(0), line, a.start(), rel)
               for a in ALIAS_RE.finditer(line, 0, m.start()) if a.start() not in excluded]
    if earlier:
        single = _single(earlier)
        if single is None:
            return [], UNRESOLVED, False, None
        return [(single, "line")], "line", False, None
    return [], _NEEDS_CONTEXT, False, None


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
        claimed: set[int] = set()
        for m in CITE_RE.finditer(line):
            if _BODY_NAME_RE.match(line, m.end()):
                # "Article 29 Working Party" names a body, not a provision.
                continue
            attributions, tier, foreign, claim = _resolve_citation(m, line, rel, poisoned, claimed)
            poisoned = poisoned or foreign
            if claim is not None:
                claimed.add(claim)
            marker = m.group("marker")
            if marker in _EXPLICIT_ONLY_MARKERS:
                if tier != "explicit":
                    continue
                attributions = [(i, t) for i, t in attributions if t == "explicit"]
            if tier == _NEEDS_CONTEXT:
                instrument, tier = _context(stack[:-1] if heading else stack, doc_instrument)
                attributions = [(instrument, tier)] if instrument is not None else []
            family = _marker_family(marker)
            if attributions and MARKER_STYLE.get(attributions[-1][0]) != family:
                # Marker-family guard: an Art-marker citation cannot belong to an
                # s.-style statute (or the reverse) — the resolved instrument is the
                # wrong one ("CCPA Article 10" is an 11 CCR regulation article), so
                # refuse rather than misattribute, at every tier.
                attributions = []
            else:
                # A conjoined prefix member of the other marker family ("SOX and
                # GDPR Articles 5(2)") is an enumeration entry alongside the
                # citation, not a co-citation of this provision: drop it.
                attributions = [(i, t) for i, t in attributions if MARKER_STYLE.get(i) == family]
            resolved_here = resolved_here or bool(attributions)
            snippet = _snippet(line, m.start(), m.end())
            for section, pinpoint, certain in expand_body(m.group("body")):
                for instrument, record_tier in (attributions if certain else []) or [(None, UNRESOLVED)]:
                    out.append(Citation(rel, lineno, m.start(), instrument, section, pinpoint,
                                        record_tier, snippet))
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
    """Normalize a typed provision to its key; None if it names no instrument.

    Accepts a key exactly as the tools print it (``PDPA (Singapore) s. 26D``,
    ``HIPAA (45 CFR) s. 164.308``: a canonical instrument name, then a
    citation of that instrument's marker family) or an explicit citation
    (``PIPEDA s.10.1(3)``, ``Singapore PDPA s. 26D``).
    """
    text = spec.strip()
    for canon in _CANONICAL_BY_LENGTH:
        if text.startswith(canon + " "):
            cite = CITE_RE.match(text, len(canon) + 1)
            if cite and _marker_family(cite.group("marker")) == MARKER_STYLE[canon]:
                sections = [s for s, _p, certain in expand_body(cite.group("body")) if certain]
                if sections:
                    return provision_key(canon, sections[0])
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
                f"'PIPEDA s. 10.1', 'GDPR Art. 33' or a key as the tools print it, "
                f"'PDPA (Singapore) s. 26D' (a bare 'Article 12(5)' names no instrument, "
                f"and an ambiguous short name needs its jurisdiction: 'Singapore PDPA "
                f"s. 26D', not 'PDPA s. 26D').",
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
