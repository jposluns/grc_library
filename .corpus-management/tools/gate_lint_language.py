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
  (the `ise_stems` profile field enumerates the stems, including prefixed derivatives;
  the rule is the Canadian-orthography form, not a generic American mandate).
- Commonwealth `-isation` noun / adjective forms (`ISATION_PATTERN`, a
  generic suffix match with the `isation_allowed_words` profile-field exclusion for the
  tiny legitimate-in-every-dialect vocabulary such as `improvisation`).
- Commonwealth `-yse` verb forms and agent nouns (the `yse_forms` profile field: analyse /
  analysed / analysing / analyser / analysers; the noun plural `analyses` is
  correct in every dialect and is not matched). Irregular-flip Commonwealth
  verbs whose Canadian form is not `-ize` (the practise-to-practice family)
  and the grammar-ambiguous verb "analyses" are caught editorially, not by
  pattern.
- Verbatim quotes of external instruments and official proper names that
  legitimately carry Commonwealth spellings are masked out of the three
  spelling checks via the `allowed_commonwealth_spans` profile field (the GDPR Article 25(1)
  quote, the OECD's official name, the WP216 opinion title, the EU / UK
  "Authorised Economic Operator" programme name).
- Bare 'ensure' or 'ensures' without 'that'. Exempt files where the rule
  itself is described (the ingestion spec, the master spec, the AI
  ingestion instruction, and governance/template-document-review-record.md).
  Verbatim external titles that carry a bare imperative 'Ensure'
  (the `verbatim_ensure_titles` profile field; currently the COBIT 2019 MEA01.05 practice
  title) are masked first, per the house-style verbatim-quote exemption.
- Section headings (H2-H6) that start with a lowercase letter after
  stripping common numbering prefixes (A1., 1.1, Step 1:, Category 1:,
  Phase, Annex). Project-name allowlist (the `lowercase_project_names` profile field:
  promptfoo, garak, pip) is permitted at the start of a heading.

Fenced code blocks are skipped for every check above.

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
import re
import sys
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
# enumerated as their own stems because the `\b(...)` construction does not
# match a covered stem inside a prefixed word. Each stem also carries its
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
    isation_allowed_words: frozenset[str]
    yse_forms: tuple[str, ...]
    allowed_commonwealth_spans: tuple[str, ...]
    verbatim_ensure_titles: tuple[str, ...]
    lowercase_project_names: set[str]


def language_vocabulary(
    *, ise_stems, isation_allowed_words, yse_forms,
    allowed_commonwealth_spans, verbatim_ensure_titles, lowercase_project_names,
) -> "LanguageVocabulary":
    """Compose raw profile arrays into the vocabulary; fail closed on bad data."""
    values = (
        ise_stems, isation_allowed_words, yse_forms,
        allowed_commonwealth_spans, verbatim_ensure_titles, lowercase_project_names,
    )
    for key, value in zip(LanguageVocabulary._fields, values):
        if not isinstance(value, list) or any(
            not isinstance(word, str) or not word for word in value
        ):
            raise ValueError(f"language.{key}: expected an array of nonempty strings")
    return LanguageVocabulary(
        tuple(ise_stems), frozenset(isation_allowed_words), tuple(yse_forms),
        tuple(allowed_commonwealth_spans), tuple(verbatim_ensure_titles),
        set(lowercase_project_names),
    )


class LanguageChecks(NamedTuple):
    vocab: LanguageVocabulary
    ise_pattern: "re.Pattern[str]"
    yse_pattern: "re.Pattern[str]"


def compile_language(vocab: LanguageVocabulary) -> LanguageChecks:
    """Compile the ise/yse spelling patterns FROM the supplied vocabulary.

    Byte-identical to the former hardcoded ISE_PATTERN / YSE_PATTERN for the
    shipped (plain-word) vocabulary: the stems carry no regex metacharacters,
    so re.escape is a no-op and the enumerated seven ise inflections match the
    former f-string construction exactly.
    """
    ise = "|".join(
        "|".join(re.escape(word) for word in (
            stem, stem + "s", stem + "d", stem[:-1] + "ing",
            stem[:-1] + "able", stem + "r", stem + "rs",
        ))
        for stem in vocab.ise_stems
    )
    yse = "|".join(re.escape(word) for word in vocab.yse_forms)
    return LanguageChecks(
        vocab,
        re.compile(r"\b(" + ise + r")\b" if ise else r"(?!)", re.IGNORECASE),
        re.compile(r"\b(" + yse + r")\b" if yse else r"(?!)", re.IGNORECASE),
    )

# Commonwealth `-isation` noun / adjective forms (organisation, authorisation,
# pseudonymisation, organisational, ...). Unlike the enumerated ise_stems verb
# stems, the noun check is a generic suffix match with a small allowed-words
# exclusion, because the legitimate-in-every-dialect `-isation` vocabulary is
# tiny (improvisation) while the Commonwealth-noun vocabulary is open-ended.
ISATION_PATTERN = re.compile(r"\b[A-Za-z][a-z]*isation(s|al|ally)?\b", re.IGNORECASE)

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

EM_DASH_PATTERN = re.compile(r"[\u2014\u2013]")  # em dash or en dash
ENSURE_PATTERN = re.compile(r"\b(ensure|ensures)\b(?!\s+that\b)", re.IGNORECASE)



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

        spelling_line = mask_allowed_spans(line, language.vocab.allowed_commonwealth_spans)
        for m in language.ise_pattern.finditer(spelling_line):
            findings.append(("ise", lineno, m.group(0)))
        for m in ISATION_PATTERN.finditer(spelling_line):
            if m.group(0).lower() not in language.vocab.isation_allowed_words:
                findings.append(("isation", lineno, m.group(0)))
        for m in language.yse_pattern.finditer(spelling_line):
            findings.append(("yse", lineno, m.group(0)))

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
        masked_value = mask_allowed_spans(value, language.vocab.allowed_commonwealth_spans)
        for m in language.ise_pattern.finditer(masked_value):
            findings.append(("ise", lineno, m.group(0)))
        for m in ISATION_PATTERN.finditer(masked_value):
            if m.group(0).lower() not in language.vocab.isation_allowed_words:
                findings.append(("isation", lineno, m.group(0)))
        for m in language.yse_pattern.finditer(masked_value):
            findings.append(("yse", lineno, m.group(0)))
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
