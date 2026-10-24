#!/usr/bin/env python3
"""Language and style audit ENGINE (Corpus-Management pack source of record).

This is the pack-owned engine for grc gate 2; the project entry point is the
thin Model-2 wrapper ``tools/lint-language.py`` (supplying the grc scan roots
and their iteration, and the language vocabulary via the ``language`` profile
since Phase-4 PR-F). Pack register ``core/gates.toml`` id ``lint-language``,
enforcing the ``language-convention`` clause. No standalone ``main()`` here for
compile PR-5 (a CLI needs the PR-6 vocabulary/config split); run via the wrapper.
The check ALGORITHM below is preserved from the former ``tools/lint-language.py``;
the vocabulary DATA moved to the ``language`` reference-vocabulary profile
(``defaults/grc/language.toml``, Phase-4 PR-F) and is passed in via run(), with the
ise/yse patterns compiled from it (byte-identical to the former hardcoded
ISE_PATTERN / YSE_PATTERN for the shipped plain-word vocabulary).

Language and style audit for the GRC Documentation Library.

The library's language convention is **Canadian English first, Commonwealth
(UK / Australian) English second, other dialects last.** Canadian English
shares its `-ize` / `-ization` orthography with American English (an
inheritance from the Oxford convention adopted in Canadian usage), but the
project's preference is named as Canadian; the `-ize` rule below is the
Canadian-orthography manifestation, not a generic American mandate. Where
Canadian English has no opinion (vocabulary or grammar features that vary
across other English dialects), Commonwealth forms are preferred; where
neither has an opinion, other dialects' usage is acceptable.

The convention is project-specific. Adopters who fork the library and want
a different convention (Commonwealth-first; American-first; etc.) can
override the `language` reference-vocabulary profile
(`defaults/grc/language.toml`) to match their own choice.

Checks for:

- Em dashes and en dashes (not allowed; replace with hyphen, colon, or
  parentheses).
- Commonwealth `-ise` verb endings used where Canadian `-ize` is preferred
  (the `ise_stems` profile field enumerates the stems; the `ise_prefixes` field
  lists verb prefixes, any run of which, with a hyphen after up to three of
  them, may precede a stem, so "reorganised", "unreorganised" and "de-emphasised" are
  reported whole while "surprise" or "premise" are not, because no listed stem
  ends them; the rule is the Canadian-orthography form, not a generic American
  mandate).
- Commonwealth `-isation` noun / adjective forms (`ISATION_PATTERN`, a
  generic suffix match with the `isation_allowed_words` profile-field exclusion for the
  tiny legitimate-in-every-dialect vocabulary such as `improvisation`).
- Commonwealth `-yse` verb forms and agent nouns (the `yse_forms` profile field: analyse /
  analysed / analysing / analyser / analysers; the noun plural `analyses` is
  correct in every dialect and is not matched). Irregular-flip Commonwealth
  verbs whose Canadian form is not `-ize` (the practise-to-practice family)
  and the grammar-ambiguous verb "analyses" are caught editorially, not by
  pattern.
- The three spelling checks bound a word by ASCII letters, not by `\\b`
  (``_NO_LETTER_BEFORE`` / ``_NO_LETTER_AFTER``): a word next to "_", a digit,
  any non-ASCII character or anything else that is not an ASCII letter is
  reported, so "_organisations_", "__organisations__", a snake_case part such as
  "data_minimisation" and "éorganisations" are flagged. Case folding is off
  inside the class, because under re.IGNORECASE `[A-Za-z]` also matches U+017F
  (long s), U+212A (Kelvin sign), U+0130 and U+0131 (dotted and dotless I).
  Residuals (false positives): a code identifier with a checked part (such as a
  function named "normalise_link") is reported, and a word with a non-ASCII
  letter inside it is reported from after that letter ("alisation" in the
  French "réalisation"). Quote such external text through the allowed spans
  below, or rename the identifier. Residual (false negative): a non-ASCII
  character inside the checked part (a ligature, a soft hyphen, a zero-width
  space or a combining mark) hides an -ise or -yse form, unless the text before
  the character is itself a complete -ise or -yse form, which is then reported
  ("recognise" in "recognise" followed by U+017F, a soft hyphen, a zero-width
  space or a combining mark and then "s"); an -isation word is
  still reported from after that character only when at least one ASCII letter
  separates the character from "isation", and is otherwise hidden too (a soft
  hyphen, a zero-width space or a combining mark directly before "isation" or
  inside it), while a character directly after "isation", before its suffix,
  leaves the word through "isation" reported ("organisation" in "organisation"
  followed by a soft hyphen and "al"). A character inside the "al" or "ally"
  suffix hides the word, except directly after the "al" of "ally", which leaves
  the word through "al" reported: "organisationa" followed by a soft hyphen and
  "l", and "organisationall" followed by a soft hyphen and "y", report nothing,
  while "organisational" followed by a soft hyphen and "ly" reports
  "organisational". Exception to both residuals: the -ise,
  -yse and -isation patterns fold case, so they match U+017F (long s) as "s",
  U+0130 and U+0131 (dotted and dotless I) as "i" and U+212A (Kelvin sign) as
  "k". An -ise or -yse form
  with one of them in place of that letter is reported ("organiſed",
  "organısed", "minimiſe", "analyſed"), and an -isation word with one of them
  anywhere before "isation" or in place of a letter of it is reported whole
  ("r", U+212A and "organisations" are reported as one word). Residual (false
  positive): an -isation word on the isation_allowed_words list with U+017F,
  U+0130 or U+0131 in it is reported ("improviſation"), because the list
  lookup lowercases the word with str.lower(), which does not map those
  characters to the plain ASCII spelling: U+017F and U+0131 stay as they are,
  and U+0130 becomes "i" followed by U+0307 (a combining dot).
- Verbatim quotes of external instruments and official proper names that
  legitimately carry Commonwealth spellings are masked out of the three
  spelling checks via the `allowed_commonwealth_spans` profile field (the GDPR Article 25(1)
  quote, the OECD's official name, the WP216 opinion title, the EU / UK
  "Authorised Economic Operator" programme name).
- Scheme-qualified http / https URL tokens are masked out of the three spelling
  checks (``mask_urls``, run before the allowed spans), because a URL is an
  external identifier whose spelling cannot be changed. The mask applies wherever
  the token occurs: bare, in an inline code span, as a link target, in a
  reference-style link definition, as an autolink, or in a generator string
  literal. Only the URL itself is masked: a link's visible text, a non-URL code
  span, and prose separated from the URL by whitespace or a delimiter are still
  checked, and the token rules (see ``URL_PATTERN``) end it where prose is glued
  to it, preferring a false positive to a bypass. The token ends at "^", at an
  ASCII control character and at any non-ASCII character, as at whitespace and
  the other stop characters. A URL opened after a "_" or "__" emphasis delimiter
  ends at a run of one or more "_" followed by anything other than an ASCII
  letter or digit, so prose after the emphasis is checked; a run of "_" followed
  by an ASCII letter or digit continues the token, as a path underscore does
  (the "___" of a path such as "/a___organisations" continues it). A "?"
  continues the token whenever a query key (any run, possibly empty, of letters,
  digits, ".", "_", "~", "+", "-" or %XX escapes) reaches "=", so
  "?-organisations=1" and "?=organisations" are masked like "?organisations=1"
  (an accepted over-mask). Residuals that stay checked (false positives): a URL
  wrapped across lines, a host with no dot or a numeric or mixed-case top-level
  label, an all-uppercase top-level label after a host label with a lowercase
  letter, a URL with userinfo, path text after a punctuation run the token rules
  end at (including the part of a dotted version such as "v1.2/" from the dot
  on), path text after a "_" (or run of "_") followed by anything other than an
  ASCII letter or digit (in an emphasized URL), text after a "_" run followed
  by anything other than an ASCII letter or digit in a URL after a literal "_"
  or "__" that is not emphasis (for example in an inline code span or a string
  literal), which is read with the emphasis rule, text after any non-ASCII
  character (not only a letter) in a URL path, query or fragment, which ends
  the token (a URL path such as "/réorganisations" reports "organisations"),
  and a URL whose host holds a non-ASCII character, which is masked only up to
  the end of the last ASCII label before the character that can end a host
  (two or more letters after a dot, under the host case rules, applied to the
  labels before the character; the letters
  directly before the character count), and not at all when no such label
  precedes it, as when the character is in the first label (since 3b366):
  an "https" URL whose host is "x.org" followed by "é", then the path
  "/organisations", is masked through "x.org" and reports "organisations",
  and "https://café.org/for-organisations" is not masked. The
  scheme is matched in ASCII only, so "httpſ://" (U+017F, long s) is not a URL
  and stays checked. Accepted over-mask: a checked
  word written as a host label, including a lowercase word glued by a dot to a
  URL with no path or an all-uppercase word glued to an all-uppercase host (a
  valid top-level label the engine cannot tell from a real one), is masked with
  the host, as is a checked word that is itself the last ASCII label before a
  non-ASCII host character and can end a host (a whole label after a dot, all
  lowercase letters, or all uppercase when no host label before the character
  holds a lowercase letter): an "https" URL whose host is "x.organisations"
  followed by "é.org", then the path "/a", is masked through
  "x.organisations". Such a word is
  reported when it is in the first label, has mixed case, or shares its label
  with a hyphen or a digit ("organisations", "x.Organisations",
  "x.a-organisations" or "x.organisations9" followed by "é.org").
- Bare 'ensure' or 'ensures' without 'that', bounded by ASCII letters like the
  spelling checks ("_ensure_", "ensure2", "éensure" and "ensure_x" are
  reported); a run of "_" or "*" may close the word before 'that' ("_ensure_
  that" passes), while emphasis on 'that' itself ("ensure _that_") is still
  reported. Exempt files where the rule
  itself is described (the ingestion spec, the master spec, the AI
  ingestion instruction, and governance/template-document-review-record.md).
  Verbatim external titles that carry a bare imperative 'Ensure'
  (the `verbatim_ensure_titles` profile field, which lists each such title) are masked
  first, per the house-style verbatim-quote exemption.
- Section headings (H2-H6) that start with a lowercase letter after
  stripping common numbering prefixes (A1., 1.1, Step 1:, Category 1:,
  Phase, Annex). Project-name allowlist (the `lowercase_project_names` profile field:
  promptfoo, garak, pip) is permitted at the start of a heading.

Fenced code blocks are skipped for every check above.

The three spelling checks run through one helper, ``spelling_matches()``: the
markdown scan, the generator-source scan below, and grc's CHANGELOG preflight
aid (``tools/preflight-changelog.py``) all share this token matcher. Their scan
contexts differ: the preflight judges added lines in isolation, so fenced
additions may be reported even though the markdown scan skips fenced blocks.

The three generators listed in GENERATOR_SOURCES emit adopter-facing
prose (audience blurbs, overview paragraphs, table cells) into the
GENERATED_DOCS artefacts, which are doubly blind to the markdown scan above:
the `.py` source is not a `.md` file, and the rendered output is excluded.
Residue: docs/reference-acquisition-manifest.md is in GENERATED_DOCS but its
generator (tools/build-reference-manifest.py) is not in GENERATOR_SOURCES, so
its emitted prose is scanned by neither half.
The generator-source scan closes that gap for those three by running the prose
house-style rules (dash, the Commonwealth-spelling checks, `ensure that`)
over each generator's
non-docstring string literals (parsed via `ast`); docstrings are developer
documentation, not emitted corpus prose, so they are excluded, and the
markdown-specific checks (heading-case) are not applied.

Usage:
    python3 tools/lint-language.py [paths...]

Exits non-zero if any findings are reported.
"""

from __future__ import annotations

import ast
import ipaddress
import re
import sys
from array import array
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-language.py), which bootstraps the vendored copy, or put "
        "the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

INGESTION_SPEC = "specification-ingestion.md"

# The authored adopter-facing guides under docs/ are in scope for this gate
# (they carry house-style prose), but the two generated artefacts there
# (docs/portal.md, docs/maturity-scorecard.md) are produced by build-portal.py
# and must not be hand-edited, so they are excluded from the scan.
GENERATED_DOCS = frozenset({"docs/portal.md", "docs/maturity-scorecard.md",
                            "docs/reference-acquisition-manifest.md"})

# The generators that emit adopter-facing prose into GENERATED_DOCS. Their
# emitted-prose string literals are scanned for the three prose house-style
# rules (dash, -ise, ensure that) so a house-style violation in
# generator-authored prose is caught at gate time rather than only at the
# next corpus-wide sweep (Sweep 78 B-1, the low-severity cleanup batch: a Commonwealth
# `customised` was hard-coded in build-portal.py, blind to the .md scan).
GENERATOR_SOURCES = (
    "tools/build-narrative-registry.py",
    "tools/build-portal.py",
    "tools/build-taxonomy.py",
)

# docs/worked-example.md is the meta-tutorial that demonstrates the
# document-creation process, so it deliberately contains examples of the very
# things other gates forbid: the
# lowercase tutorial step headings ("## Step 1: pick the document type"), and
# the word "ensure" while teaching the ensure-that rule. It is therefore exempt
# from the heading-case and ensure checks (the same
# meta-demonstration exemption the AI ingestion instruction already carries for
# "ensure"); dash and -ise enforcement still apply.
WORKED_EXAMPLE = "docs/worked-example.md"

# Each stem carries all four regular inflections of the Commonwealth `-ise`
# verb: base (`-ise`), third-person singular (`-ises`), past / participle
# (`-ised`), and present participle (`-ising`). The `-ises` form was added
# 2026-06-30 (#480 /validate-pr finding: `recognises` and the other
# third-person forms passed gate 2 because only three of the four inflections
# were listed); keep all four present for any stem added later. Prefixed
# derivatives (unauthorised, unrecognised, reorganise, deprioritise, ...) are
# matched through the `ise_prefixes` list (3b234 round 4): the letter-bounded
# construction does not match a covered stem inside a prefixed word, so any run
# of listed prefixes, with a hyphen after up to three of them, may precede a stem
# inside the same bounds. Only the base stem is listed; a prefixed word that is
# not a run of listed prefixes before a listed stem (immobilise) is listed as its
# own stem. A word is only matched when a listed stem ends it, so a word that
# merely begins with a prefix (premise, devise, comprise, disguise) is never
# reported. Each stem also carries its
# derivational forms: the -isable adjective and the -iser / -isers agent
# nouns (a false-negative verifier on the 2026-07-02 harmonization sweep
# found the derivational family escaping both the sweep and the gate). The
# verb form "analyses" (vs the every-dialect noun plural of "analysis") is
# grammar-ambiguous and deliberately NOT matched; it is caught editorially.
class LanguageVocabulary(NamedTuple):
    """The adopter-overridable language vocabulary (Phase-4 PR-F).

    The check ALGORITHM stays in this engine; only these vocabulary DATA sets
    move to the ``language`` reference-vocabulary profile and are passed in.
    """
    ise_stems: tuple[str, ...]
    ise_prefixes: tuple[str, ...]
    isation_allowed_words: frozenset[str]
    yse_forms: tuple[str, ...]
    allowed_commonwealth_spans: tuple[str, ...]
    verbatim_ensure_titles: tuple[str, ...]
    lowercase_project_names: set[str]


def language_vocabulary(
    *, ise_stems, ise_prefixes, isation_allowed_words, yse_forms,
    allowed_commonwealth_spans, verbatim_ensure_titles, lowercase_project_names,
) -> "LanguageVocabulary":
    """Compose raw profile arrays into the vocabulary; fail closed on bad data.

    Every field is required (a missing one raises TypeError). A prefix must be
    ASCII letters only: the optional hyphen after it is the engine's, and any
    other character would break the letter bounds of the word.
    """
    values = (
        ise_stems, ise_prefixes, isation_allowed_words, yse_forms,
        allowed_commonwealth_spans, verbatim_ensure_titles, lowercase_project_names,
    )
    for key, value in zip(LanguageVocabulary._fields, values):
        if not isinstance(value, list) or any(
            not isinstance(word, str) or not word for word in value
        ):
            raise ValueError(f"language.{key}: expected an array of nonempty strings")
    if any(not re.fullmatch(r"[A-Za-z]+", prefix) for prefix in ise_prefixes):
        raise ValueError("language.ise_prefixes: expected ASCII letters only")
    return LanguageVocabulary(
        tuple(ise_stems), tuple(ise_prefixes), frozenset(isation_allowed_words),
        tuple(yse_forms),
        tuple(allowed_commonwealth_spans), tuple(verbatim_ensure_titles),
        set(lowercase_project_names),
    )


class IsePrefixScan(NamedTuple):
    """The ise pattern split into parts for the linear-time scan (3b234 round 6)."""
    start: "re.Pattern[str]"
    prefixes: tuple["re.Pattern[str]", ...]
    stem: "re.Pattern[str]"


class LanguageChecks(NamedTuple):
    vocab: LanguageVocabulary
    ise_pattern: "re.Pattern[str]"
    yse_pattern: "re.Pattern[str]"
    ise_scan: "IsePrefixScan | None" = None


# The three spelling checks bound a word by ASCII letters, not by `\b` (3b372):
# `\b` treats "_", digits and non-ASCII letters as word characters, so a word
# in "_" / "__" emphasis, in a snake_case name, glued to a digit or glued to a
# non-ASCII letter ("_organisations_", "éorganisations") was not reported. The
# class is ASCII-only and case-folding is switched off inside it, because under
# re.IGNORECASE `[A-Za-z]` also matches U+017F (long s), U+212A (Kelvin sign),
# U+0130 and U+0131 (dotted and dotless I). A non-ASCII character inside the
# checked part (a ligature, soft hyphen, zero-width space or combining mark)
# hides an -ise or -yse form, unless the text before the character is itself a
# complete -ise or -yse form, which is reported ("recognise" + U+017F + "s"
# reports "recognise"); an -isation word is still reported from after
# that character only when at least one ASCII letter separates the character
# from "isation", and is otherwise hidden too (a residual), while a character
# directly after "isation", before its suffix, leaves the word through
# "isation" reported ("organisation" + U+00AD + "al" reports "organisation").
# A character inside the "al" or "ally" suffix hides the word, except directly
# after the "al" of "ally", which leaves the word through "al" reported
# ("organisationa" + U+00AD + "l" and "organisationall" + U+00AD + "y" report
# nothing; "organisational" + U+00AD + "ly" reports "organisational").
# The patterns themselves still fold case, so they match U+017F as "s", U+0130
# and U+0131 as "i" and U+212A as "k": an -ise or -yse form with one of them in
# place of that letter is reported ("organiſed", "analyſed"), and an -isation
# word with one of them anywhere before "isation" or in place of a letter of it
# is reported whole.
# The isation_allowed_words lookup uses str.lower(), which does not map U+017F,
# U+0130 or U+0131 to the plain ASCII spelling (U+017F and U+0131 stay as they
# are; U+0130 becomes "i" + U+0307, a combining dot), so an allowed word holding
# one of them is reported ("improviſation", a residual false positive).
_NO_LETTER_BEFORE = r"(?<!(?-i:[A-Za-z]))"
_NO_LETTER_AFTER = r"(?!(?-i:[A-Za-z]))"


def compile_language(vocab: LanguageVocabulary) -> LanguageChecks:
    """Compile the ise/yse spelling patterns FROM the supplied vocabulary.

    The alternation is the former hardcoded ISE_PATTERN / YSE_PATTERN one for
    the shipped (plain-word) vocabulary: the stems carry no regex metacharacters,
    so re.escape is a no-op and the enumerated seven ise inflections match the
    former f-string construction exactly. Since 3b372 it is bounded by
    ``_NO_LETTER_BEFORE`` / ``_NO_LETTER_AFTER`` instead of ``\\b``. Since 3b234
    round 4 any run of ``ise_prefixes`` may precede the stem inside those bounds,
    with a "-" after up to three of them, and the whole word, prefixes included,
    is reported; a chain with more hyphens is reported from its last three
    hyphenated groups. With no prefixes listed the pattern is the one above.
    With prefixes listed, ``ise_words`` runs the pattern through ``ise_scan``
    (3b234 round 6), which reports exactly what the pattern reports. An empty
    prefix or stem raises ValueError (3b407): ``language_vocabulary`` already
    rejects one, but a vocabulary built directly would otherwise reach the scan.
    """
    if any(not prefix for prefix in vocab.ise_prefixes):
        raise ValueError("ise_prefixes: expected nonempty prefixes")
    if any(not stem for stem in vocab.ise_stems):
        raise ValueError("ise_stems: expected nonempty stems")
    stems = "|".join(
        "|".join(re.escape(word) for word in (
            stem, stem + "s", stem + "d", stem[:-1] + "ing",
            stem[:-1] + "able", stem + "r", stem + "rs",
        ))
        for stem in vocab.ise_stems
    )
    ise = stems
    scan = None
    prefixes = "|".join(re.escape(prefix) for prefix in vocab.ise_prefixes)
    if stems and prefixes:
        # At most three hyphenated groups: an unbounded hyphenated run would be
        # retried from every hyphen of a long prefix chain (quadratic time).
        ise = ("(?:(?:" + prefixes + ")+-){0," + str(_ISE_HYPHEN_GROUPS) + "}(?:"
               + prefixes + ")*(?:" + stems + ")")
        scan = IsePrefixScan(
            re.compile(_NO_LETTER_BEFORE + "(?=" + prefixes + "|" + stems + ")",
                       re.IGNORECASE),
            tuple(re.compile(re.escape(prefix), re.IGNORECASE)
                  for prefix in vocab.ise_prefixes),
            re.compile("(?:" + stems + ")" + _NO_LETTER_AFTER, re.IGNORECASE),
        )
    yse = "|".join(re.escape(word) for word in vocab.yse_forms)
    return LanguageChecks(
        vocab,
        re.compile(_NO_LETTER_BEFORE + "(" + ise + ")" + _NO_LETTER_AFTER
                   if ise else r"(?!)", re.IGNORECASE),
        re.compile(_NO_LETTER_BEFORE + "(" + yse + ")" + _NO_LETTER_AFTER
                   if yse else r"(?!)", re.IGNORECASE),
        scan,
    )


# The ise pattern with prefixes is quadratic in Python's backtracking engine on a
# long prefix run holding a character that folds to an ASCII letter of a prefix
# (3b234 round 6): in "mi\u017f" * n + "x" (U+017F, long s, folds to "s") the pattern
# consumes the whole run as prefixes, and because the ASCII-only letter bound
# allows a fresh attempt after every U+017F, each attempt walks the rest of the
# run again (about 29 seconds for n = 4000). U+0130 and U+0131 (dotted and
# dotless I) do the same for prefixes holding "i". ``ise_words`` therefore runs
# the same pattern as a memoized search: each state (a position, the hyphenated
# groups used so far, and the part of the pattern being matched) is solved once
# per text, in the backtracking engine's order (more prefixes before fewer, a
# further hyphenated group before the unhyphenated run, prefixes and stem forms
# in listed order), so it reports the same words as the pattern in time linear
# in the length of the text. The memo and the search stack hold small integers
# (3b407): the tuple-keyed memo and the list frames of round 6 cost about 250 MB
# for a one-line word of a million characters, the arrays below about 10 MB.
_ISE_HYPHEN_GROUPS = 3

# The parts of an ise_words state, in its two low bits; "S" is never stacked.
_ISE_G, _ISE_H0, _ISE_H1, _ISE_T, _ISE_S = range(5)


def ise_words(text: str, language: LanguageChecks) -> list[str]:
    """The words the ise pattern reports in ``text``, in order (3b234 round 6)."""
    scan = language.ise_scan
    if scan is None:
        return [m.group(0) for m in language.ise_pattern.finditer(text)]
    # A state is (part, hyphenated groups used, position). "G": before another
    # hyphenated group or the unhyphenated run; "H0" / "H1": inside a hyphenated
    # group before / after its first prefix; "T": inside the unhyphenated run;
    # "S": a stem form with the letter bound after it. "T" and "S" do not depend
    # on the groups used, so they carry 0. Only "H1" and "T" states can be
    # reached twice, and a success ends the search from its start position with
    # every later start at or after the word's end, so the memo records only
    # failures: bit 0 of failed[x] for "T" at x, bit 1 + g for "H1" at x after g
    # hyphenated groups.
    prefixes = scan.prefixes
    count = len(prefixes)
    failed = bytearray(len(text) + 1)

    def next_child(part, groups, x, index):
        """The first child of a state at or after ``index``, with the index after it."""
        if part == _ISE_G:
            if index == 0 and groups < _ISE_HYPHEN_GROUPS:
                return _ISE_H0, groups, x, 1
            if index < 2:
                return _ISE_T, 0, x, 2
            return None
        while index < count:
            m = prefixes[index].match(text, x)
            index += 1
            # A zero-width prefix match would make the state its own child and
            # loop without end (3b407); compile_language rejects empty prefixes.
            if m and m.end() > x:
                return _ISE_T if part == _ISE_T else _ISE_H1, groups, m.end(), index
        if index == count:
            if part == _ISE_T:
                return _ISE_S, 0, x, count + 1
            if part == _ISE_H1 and text.startswith("-", x):
                return _ISE_G, groups + 1, x + 1, count + 1
        return None

    def solve(root):
        # Two integers per frame: the state (position << 4 | groups << 2 | part)
        # and the index of its next child.
        stack = array("q", (root << 4 | _ISE_G, 0))
        while stack:
            index = stack.pop()
            state = stack[-1]
            part, groups, x = state & 3, state >> 2 & 3, state >> 4
            child = next_child(part, groups, x, index)
            if child is None:
                stack.pop()
                if part == _ISE_T:
                    failed[x] |= 1
                elif part == _ISE_H1:
                    failed[x] |= 2 << groups
                continue
            part, groups, x, index = child
            stack.append(index)
            if part == _ISE_S:
                m = scan.stem.match(text, x)
                if m:
                    return m.end()
            elif not (part == _ISE_T and failed[x] & 1
                      or part == _ISE_H1 and failed[x] & 2 << groups):
                stack.append(x << 4 | groups << 2 | part)
                stack.append(0)
        return None

    words = []
    pos = 0
    # Every start moves pos past it, even when its word is zero-width (a
    # hand-built stem pattern that matches empty), and search() reads a pos past
    # the end as the end, so the loop stops there (3b407 round 2).
    while pos <= len(text) and (m := scan.start.search(text, pos)) is not None:
        end = solve(m.start())
        if end is None:
            pos = m.start() + 1
        else:
            words.append(text[m.start():end])
            pos = max(end, m.start() + 1)
    return words

# Commonwealth `-isation` noun / adjective forms (organisation, authorisation,
# pseudonymisation, organisational, ...). Unlike the enumerated ise_stems verb
# stems, the noun check is a generic suffix match with a small allowed-words
# exclusion, because the legitimate-in-every-dialect `-isation` vocabulary is
# tiny (improvisation) while the Commonwealth-noun vocabulary is open-ended.
ISATION_PATTERN = re.compile(
    _NO_LETTER_BEFORE + r"[A-Za-z][a-z]*isation(s|al|ally)?" + _NO_LETTER_AFTER, re.IGNORECASE)

# Commonwealth `-yse` verb forms and agent nouns (Canadian is `analyze` /
# `analyzer`). The noun plural `analyses` (of `analysis`) is deliberately NOT
# matched: it is correct in every dialect and indistinguishable from the
# verb's third-person form only by grammar, so the pattern lists the
# unambiguous inflections.

# Verbatim Commonwealth-spelling spans are masked out of a line before the three
# spelling checks run (dash / ensure / heading checks are unaffected). The spans
# themselves live in the ``allowed_commonwealth_spans`` field of the ``language``
# reference-vocabulary profile (``defaults/grc/language.toml``) since Phase-4 PR-F;
# add one ONLY for a verbatim quote of an external instrument or an official proper
# name, never for ordinary prose. The shipped four are the GDPR Article 25(1)
# official-text quote, the OECD's official English name, the Article 29 Working
# Party opinion's official title, and the EU / UK "Authorised Economic Operator"
# customs programme name.


def mask_allowed_spans(line: str, spans: tuple[str, ...]) -> str:
    """Blank out the supplied verbatim Commonwealth spans before spelling checks."""
    for span in spans:
        if span in line:
            line = line.replace(span, " " * len(span))
    return line


# Scheme-qualified http(s) URL tokens are masked out of the three spelling checks
# (3b366): a URL is an external identifier whose spelling the library cannot change
# (the UK ICO `for-organisations` guidance path). The mask applies wherever the token
# occurs (a bare URL, an inline code span, a link target, a reference-style link
# definition, an autolink, a generator string literal). The scheme (any case, ASCII
# letters only: "httpſ" with U+017F, long s, is not a scheme, 3b372) must be
# preceded by a non-word character or by a "_" or "__" emphasis delimiter that is
# itself preceded by a non-word character ("_https://" is recognized, "xhttps://"
# and "x_https://" are not), and followed by a real authority: dot-separated host
# labels ending in an all-lowercase alphabetic top-level label, or in an all-uppercase
# one when no host label contains a lowercase letter (the host "X.ORG.UK" is
# accepted, while "ico.org.uk.ORGANISATIONS" ends the host at ".uk"), or a bracketed literal
# that the standard library's ipaddress module accepts as an IPv6 address, with an
# optional port. The token then takes only a path, query or fragment starting with
# "/", "?" or "#", and stops at whitespace, a backtick, "<", ">", a double quote,
# "|", "*", "{", "}", a square bracket, a backslash, "^", "~~", a "%" not followed by
# two hexadecimal digits, an ASCII control character, any non-ASCII character and
# an unbalanced parenthesis; one level of balanced parentheses inside the path is
# kept. When the scheme follows a "_" or "__" emphasis delimiter, a run of one or
# more "_" continues the token only when an ASCII letter or digit follows the run
# (each "_" is kept only when, after any further "_", an ASCII letter or digit
# follows), so the closing delimiter ends it when followed by anything other than
# an ASCII letter or digit (a URL in "_..._(organisations)" or "_..._#organisations"
# leaves the text after the delimiter checked, while the "___" of a path such as
# "/a___organisations" continues the token); a "_" or run of "_" in the path (the
# "_" of "/a_b/c_" or "/v_2/c_" in a URL opened after "_") is kept only when an
# ASCII letter or digit follows it, so a path "_" followed by anything else,
# punctuation or a non-ASCII letter alike, ends the token (in
# "/for_/organisations/x_" the text from that "_" on stays checked, a residual);
# without the delimiter "_" is an ordinary path character. The rule reads the
# text, not markdown, so a URL after a literal "_" or "__" that is not emphasis
# (for example in an inline code span or a string literal) is read with the
# emphasis rule too, and text after a "_" run followed by anything other than an
# ASCII letter or digit in a URL after a literal "_" or "__" stays checked (a
# residual). Prose glued to the URL is left to the checks by
# preferring under-masking (a false positive) to over-masking (a bypass): one of
# ".,;:!?" continues the token only when no letter, "-", "_", "~", "+", "@", "$",
# apostrophe, "(", ")", "&", "%", "=", "#" or "/" follows, directly or after a
# run of digits (",1-organisations",
# ",1/organisations" and "a(b,)organisations" end; so does "v1.2/", a residual; the
# ":" of a nested "http://" or "https://" continues); a dot followed by letters
# continues it only as a lowercase extension of one to six characters ending the
# segment (".html", ".pdf"; every checked word is at least seven letters), so
# ".The-organisation" and ".Organisations" end the token; "?" continues it whenever
# a query key, any run (possibly empty) of letters, digits, ".", "_", "~", "+", "-"
# or %XX escapes, reaches "=" ("?organisations=1", "?-organisations=1" and
# "?=organisations" are masked, an accepted over-mask) and otherwise ends it; an
# apostrophe continues it only as a possessive "'s". The trailing ".,;:!?" is then
# trimmed from the token and left unmasked. Residuals (under-masked, so they fail
# safe as false positives): a URL wrapped across lines, a host with no dot or a
# numeric or mixed-case top-level label, an all-uppercase top-level label after a
# host label with a lowercase letter, a URL with userinfo, path text after a
# punctuation run the rules above end the token at (including the part of a dotted
# version such as "v1.2/" from the dot on), path text after a "_" (or run of "_")
# followed by anything other than an ASCII letter or digit (in an emphasized URL),
# text after a "_" run followed by anything other than an ASCII letter or digit in
# a URL after a literal "_" or "__" that is not emphasis (for example in an inline
# code span or a string literal), which is read with the emphasis rule, text after
# any non-ASCII character (not only a letter) in a URL path, query or fragment,
# which ends the token (a URL path such as "/réorganisations" reports
# "organisations"), and a URL whose host holds a non-ASCII character, which is
# masked only up to the end of the last ASCII label before the character that
# _URL_HOST accepts as a top-level label (the letters directly before the
# character count), and not at all when no such label precedes it, as when the
# character is in the first label (since 3b366): an "https" URL whose host is
# "x.org" followed by "é", then the path "/organisations", is masked through
# "x.org" and reports "organisations", and "https://café.org/for-organisations"
# is not masked.
# Accepted over-mask (besides the query-key forms above): a host is masked as
# written, so a checked word spelled as a host label is not reported, including a
# lowercase word glued by a dot to a URL with no path or an all-uppercase word glued
# to an all-uppercase host, which is a syntactically valid top-level label that the
# engine cannot tell from a real one without a top-level-domain registry, and a
# checked word that is itself the last ASCII label before a non-ASCII host
# character and that _URL_HOST accepts as a top-level label (an "https" URL whose
# host is "x.organisations" followed by "é.org", then the path "/a", is masked
# through "x.organisations"); a checked word in the first label, in mixed case or
# sharing its label with a hyphen or a digit ("x.Organisations",
# "x.a-organisations" or "x.organisations9" followed by "é.org") is reported.
_URL_SAFE = (r"(?:[A-Za-z0-9\-=&+#@$/]|(?(emph)_(?=_*[A-Za-z0-9])|_)"
             r"|~(?!~)|%[0-9A-Fa-f]{2})")
_URL_PUNCT = (r"(?:[.,;:!?](?![A-Za-z\-_~+@$'()&%=#/]|[0-9]+[A-Za-z\-_~+@$'()&%=#/])"
              r"|(?<=[Hh][Tt][Tt][Pp]):(?=//)|(?<=[Hh][Tt][Tt][Pp][Ss]):(?=//))")
_URL_EXT = r"\.(?=[a-z][a-z0-9]{0,5}(?![A-Za-z0-9\-_]))"
_URL_QUERY = r"\?(?=(?:[A-Za-z0-9_.~+\-]|%[0-9A-Fa-f]{2})*=)"
_URL_APOS = r"'(?=s(?![A-Za-z]))"
_URL_CHAR = f"(?:{_URL_SAFE}|{_URL_PUNCT}|{_URL_EXT}|{_URL_QUERY}|{_URL_APOS})"
_URL_HOST = (r"(?:\[(?P<ipv6>[0-9A-Fa-f:.]+)\]"
             r"|(?:[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?\.)+[a-z]{2,63}(?![A-Za-z0-9\-])"
             r"|(?:[A-Z0-9](?:[A-Z0-9\-]*[A-Z0-9])?\.)+[A-Z]{2,63}(?![A-Za-z0-9\-]))"
             r"(?::[0-9]{1,5})?")
URL_PATTERN = re.compile(
    r"(?:(?<!\w)|(?P<emph>)(?:(?<=(?<!\w)_)|(?<=(?<!\w)__)))(?ai:https?)://" + _URL_HOST
    + rf"(?:(?:[/#]|{_URL_QUERY})(?:{_URL_CHAR}|\({_URL_CHAR}*\))*)?")
URL_TRAILING_PUNCTUATION = ".,;:!?"


def _blank_url(match: "re.Match[str]") -> str:
    token = match.group(0)
    if match.group("ipv6") is not None:
        try:
            ipaddress.IPv6Address(match.group("ipv6"))
        except ValueError:
            return token
    kept = token.rstrip(URL_TRAILING_PUNCTUATION)
    return " " * len(kept) + token[len(kept):]


def mask_urls(line: str) -> str:
    """Blank out scheme-qualified http(s) URL tokens before spelling checks."""
    return URL_PATTERN.sub(_blank_url, line)


def spelling_matches(text: str, language: LanguageChecks) -> list[tuple[str, str]]:
    """The three spelling checks on one line or string literal, as ``(kind, word)``.

    Kinds are ``ise``, ``isation`` and ``yse``, reported in that order, after any
    http(s) URL tokens (``mask_urls``) and then the allowed Commonwealth spans are
    masked; URLs go first so an allowed span inside a URL cannot split it. This is
    the single spelling loop: check_file, check_generator_source and the grc
    CHANGELOG preflight aid call it.
    """
    masked = mask_allowed_spans(mask_urls(text), language.vocab.allowed_commonwealth_spans)
    found = [("ise", word) for word in ise_words(masked, language)]
    found += [("isation", m.group(0)) for m in ISATION_PATTERN.finditer(masked)
              if m.group(0).lower() not in language.vocab.isation_allowed_words]
    found += [("yse", m.group(0)) for m in language.yse_pattern.finditer(masked)]
    return found

EM_DASH_PATTERN = re.compile(r"[\u2014\u2013]")  # em dash or en dash
# The ensure check uses the same ASCII-letter bounds as the spelling checks
# (3b372), so "_ensure_", "ensure2", "éensure" and "ensure_x" are reported; a run
# of "_" or "*" emphasis may close the word before "that" ("_ensure_ that"), while
# emphasis on "that" itself ("ensure _that_") is still reported.
ENSURE_PATTERN = re.compile(
    _NO_LETTER_BEFORE + r"(ensure|ensures)" + _NO_LETTER_AFTER + r"(?![_*]*\s+that\b)",
    re.IGNORECASE)



def mask_verbatim_ensure_titles(line: str, spans: tuple[str, ...]) -> str:
    """Blank out the supplied verbatim ensure-titles before the ensure-that check."""
    for span in spans:
        if span in line:
            line = line.replace(span, " " * len(span))
    return line
HEADING_PATTERN = re.compile(r"^(#{2,6})\s+(.+?)\s*$")

NUMBERING_PATTERNS = [
    re.compile(r"^\d+(\.\d+)*\.?\s+"),       # 1., 1.1, 1.1.1
    re.compile(r"^[A-Z]\d+(\.\d+)?\.?\s+"),  # A1, B2.3
    re.compile(r"^Step\s+\d+\s*:\s*", re.IGNORECASE),
    re.compile(r"^Category\s+\d+\s*:\s*", re.IGNORECASE),
    re.compile(r"^Phase\s+\d+\s*:\s*", re.IGNORECASE),
    re.compile(r"^Annex\s+[A-Z]\.?\s+"),
]



def strip_numbering(text: str) -> str:
    """Strip a single leading numbering prefix; do not recurse."""
    for pattern in NUMBERING_PATTERNS:
        m = pattern.match(text)
        if m:
            return text[m.end():]
    return text


def filter_markdown_files(files: list[Path], repo_root: Path) -> list[Path]:
    # Exclude the generated docs/ artefacts (build-portal.py output); they are
    # not hand-authored prose and are kept in sync by their own --check gate.
    # (Scan-root iteration is the project wrapper's job; only the GENERATED_DOCS
    # subtraction stays with the engine.)
    return [f for f in files if f.relative_to(repo_root).as_posix() not in GENERATED_DOCS]


def check_file(path: Path, repo_root: Path, *,
               language: LanguageChecks) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    relative = path.relative_to(repo_root).as_posix()
    is_ingestion_spec = relative == INGESTION_SPEC
    is_master_spec = relative == "specification-master-project.md"
    is_instruction_file = relative == "instruction-ai-document-ingestion.md"
    is_review_record_template = relative == "governance/template-document-review-record.md"
    is_worked_example = relative == WORKED_EXAMPLE

    file_text = read_text_safe(path)
    if file_text is None:
        return findings
    for lineno, line in iter_non_code_lines(file_text):
        if EM_DASH_PATTERN.search(line):
            findings.append(("dash", lineno, line.strip()))

        for kind, word in spelling_matches(line, language):
            findings.append((kind, lineno, word))

        # Skip the specs', the AI ingestion instruction's, and the document review
        # record template's own self-referential rule statements about "ensure that".
        if (not is_ingestion_spec and not is_master_spec and not is_instruction_file
                and not is_review_record_template and not is_worked_example
                and ENSURE_PATTERN.search(mask_verbatim_ensure_titles(
                    line, language.vocab.verbatim_ensure_titles))):
            findings.append(("ensure", lineno, line.strip()))

        heading = HEADING_PATTERN.match(line)
        if heading and not is_worked_example:
            _, heading_text = heading.groups()
            stem = strip_numbering(heading_text)
            if stem and stem[0].islower():
                # Allow canonical lowercase project names as first word.
                first_word = re.split(r"\s|[^A-Za-z0-9_-]", stem, maxsplit=1)[0].lower()
                if first_word not in language.vocab.lowercase_project_names:
                    findings.append(("heading-case", lineno, line.strip()))

    return findings


def _docstring_constant_ids(tree: ast.AST) -> set[int]:
    """Return the id()s of Constant nodes that are module/def/class docstrings.

    A docstring is the first statement of a module, function, async
    function, or class body when that statement is an expression wrapping a
    string constant. Docstrings are developer documentation, not prose
    emitted into the corpus, so the generator-source scan excludes them.
    """
    ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", None)
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                ids.add(id(body[0].value))
    return ids


def check_generator_source(path: Path, *,
                           language: LanguageChecks) -> list[tuple[str, int, str]]:
    """Scan a build-*.py generator's non-docstring string literals.

    Runs the three prose house-style rules (dash, -ise, ensure that) over
    every string-constant literal that is not a docstring. The markdown-only
    checks (heading-case) are not applied: generators
    emit navigation prose and tables, not the ingested-content or
    heading-cased forms those rules target.
    """
    findings: list[tuple[str, int, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        findings.append(("syntax", getattr(exc, "lineno", 0) or 0,
                         f"could not parse {path.name}: {exc.msg}"))
        return findings
    docstring_ids = _docstring_constant_ids(tree)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        lineno = getattr(node, "lineno", 0)
        if EM_DASH_PATTERN.search(value):
            findings.append(("dash", lineno, value.strip()[:160]))
        for kind, word in spelling_matches(value, language):
            findings.append((kind, lineno, word))
        if ENSURE_PATTERN.search(mask_verbatim_ensure_titles(value, language.vocab.verbatim_ensure_titles)):
            findings.append(("ensure", lineno, value.strip()[:160]))
    return findings


def run(md_files: list[Path], gen_input: list[str], *, repo_root: Path,
        vocab: LanguageVocabulary) -> int:
    language = compile_language(vocab)
    files = filter_markdown_files(md_files, repo_root)
    # Generator sources are scanned for the emitted-prose house-style rules;
    # routed by suffix so an explicit .py argument (a regression fixture) is
    # checked here while an explicit .md argument is checked as markdown.
    gen_files = [
        f for f in sorted({(repo_root / p) for p in gen_input if (repo_root / p).suffix == ".py"})
        if f.is_file()
    ]

    grouped: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f, repo_root, language=language):
            grouped[f.relative_to(repo_root).as_posix()].append(finding)
            total += 1
    for f in gen_files:
        for finding in check_generator_source(f, language=language):
            grouped[f.relative_to(repo_root).as_posix()].append(finding)
            total += 1

    if not grouped:
        print("OK: no language findings.")
        return 0

    for relpath in sorted(grouped):
        print(f"=== {relpath} ===")
        # Suppress duplicates per file for readability.
        seen = set()
        for kind, lineno, snippet in grouped[relpath]:
            key = (kind, lineno, snippet)
            if key in seen:
                continue
            seen.add(key)
            print(f"  L{lineno} [{kind}] {snippet[:160]}")

    print(f"\nFAIL: {total} finding(s) across {len(grouped)} file(s).")
    return 1
