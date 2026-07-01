#!/usr/bin/env python3
"""Language and style audit for the GRC Documentation Library.

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
modify `ISE_PATTERN` below to match their own choice.

Checks for:

- Em dashes and en dashes (not allowed; replace with hyphen, colon, or
  parentheses).
- Commonwealth `-ise` endings used where Canadian `-ize` is preferred
  (`ISE_PATTERN` enumerates the word list; the rule is the Canadian-
  orthography form, not a generic American mandate).
- Bare 'ensure' or 'ensures' without 'that'. Exempt files where the rule
  itself is described (the ingestion spec, the master spec, the AI
  ingestion instruction, and governance/template-document-review-record.md).
- Section headings (H2-H6) that start with a lowercase letter after
  stripping common numbering prefixes (A1., 1.1, Step 1:, Category 1:,
  Phase, Annex). Project-name allowlist (LOWERCASE_PROJECT_NAMES:
  promptfoo, garak, pip) is permitted at the start of a heading.
- Sanitization-table source terms (SANITISATION_TERMS) appearing outside
  the ingestion specification.

Fenced code blocks are skipped for every check above.

The `tools/build-*.py` generators (GENERATOR_SOURCES) emit adopter-facing
prose (audience blurbs, overview paragraphs, table cells) into the
GENERATED_DOCS artefacts, which are doubly blind to the markdown scan above:
the `.py` source is not a `.md` file, and the rendered output is excluded.
The generator-source scan closes that gap by running the three prose
house-style rules (dash, `-ise`, `ensure that`) over each generator's
non-docstring string literals (parsed via `ast`); docstrings are developer
documentation, not emitted corpus prose, so they are excluded, and the
markdown-specific checks (heading-case, sanitisation) are not applied.

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

from lint_common import AUDITED_DOMAIN_DIRS, iter_non_code_lines, read_text_safe

REPO_ROOT = Path(__file__).resolve().parent.parent
INGESTION_SPEC = "specification-ingestion.md"

# The authored adopter-facing guides under docs/ are in scope for this gate
# (they carry house-style prose), but the two generated artefacts there
# (docs/portal.md, docs/maturity-scorecard.md) are produced by build-portal.py
# and must not be hand-edited, so they are excluded from the scan.
GENERATED_DOCS = frozenset({"docs/portal.md", "docs/maturity-scorecard.md"})

# The generators that emit adopter-facing prose into GENERATED_DOCS. Their
# emitted-prose string literals are scanned for the three prose house-style
# rules (dash, -ise, ensure that) so a house-style violation in
# generator-authored prose is caught at gate time rather than only at the
# next corpus-wide sweep (TODO 3.14 / Sweep 78 B-1: a Commonwealth
# `customised` was hard-coded in build-portal.py, blind to the .md scan).
GENERATOR_SOURCES = (
    "tools/build-portal.py",
    "tools/build-taxonomy.py",
)

# docs/worked-example.md is the meta-tutorial that demonstrates the
# document-creation process, so it deliberately contains examples of the very
# things other gates forbid: vendor names it shows being sanitised, the
# lowercase tutorial step headings ("## Step 1: pick the document type"), and
# the word "ensure" while teaching the ensure-that rule. It is therefore exempt
# from the heading-case, sanitisation, and ensure checks (the same
# meta-demonstration exemption the AI ingestion instruction already carries for
# "ensure"); dash and -ise enforcement still apply.
WORKED_EXAMPLE = "docs/worked-example.md"

# Each stem carries all four regular inflections of the Commonwealth `-ise`
# verb: base (`-ise`), third-person singular (`-ises`), past / participle
# (`-ised`), and present participle (`-ising`). The `-ises` form was added
# 2026-06-30 (#480 /validate-pr finding: `recognises` and the other
# third-person forms passed gate 2 because only three of the four inflections
# were listed); keep all four present for any stem added later.
ISE_PATTERN = re.compile(
    r"\b("
    r"recognise|recognises|recognised|recognising|"
    r"organise|organises|organised|organising|"
    r"prioritise|prioritises|prioritised|prioritising|"
    r"categorise|categorises|categorised|categorising|"
    r"emphasise|emphasises|emphasised|emphasising|"
    r"harmonise|harmonises|harmonised|harmonising|"
    r"standardise|standardises|standardised|standardising|"
    r"optimise|optimises|optimised|optimising|"
    r"centralise|centralises|centralised|centralising|"
    r"customise|customises|customised|customising|"
    r"finalise|finalises|finalised|finalising|"
    r"specialise|specialises|specialised|specialising|"
    r"utilise|utilises|utilised|utilising|"
    r"minimise|minimises|minimised|minimising|"
    r"maximise|maximises|maximised|maximising|"
    r"criticise|criticises|criticised|criticising|"
    r"generalise|generalises|generalised|generalising|"
    r"operationalise|operationalises|operationalised|operationalising"
    r")\b",
    re.IGNORECASE,
)

EM_DASH_PATTERN = re.compile(r"[—–]")  # em dash or en dash
ENSURE_PATTERN = re.compile(r"\b(ensure|ensures)\b(?!\s+that\b)", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"^(#{2,6})\s+(.+?)\s*$")

NUMBERING_PATTERNS = [
    re.compile(r"^\d+(\.\d+)*\.?\s+"),       # 1., 1.1, 1.1.1
    re.compile(r"^[A-Z]\d+(\.\d+)?\.?\s+"),  # A1, B2.3
    re.compile(r"^Step\s+\d+\s*:\s*", re.IGNORECASE),
    re.compile(r"^Category\s+\d+\s*:\s*", re.IGNORECASE),
    re.compile(r"^Phase\s+\d+\s*:\s*", re.IGNORECASE),
    re.compile(r"^Annex\s+[A-Z]\.?\s+"),
]

# Canonical lowercase project names that may appear as the first word of a heading.
LOWERCASE_PROJECT_NAMES = {
    "promptfoo",
    "garak",
    "pip",  # the trusted-trader programme acronym is uppercase; lowercase 'pip' is the Python installer
}

SANITISATION_TERMS = [
    "Traffic Tech",
    "Mississauga data centre",
    "MissDC",
    "Microsoft Entra",
    "Entra ID",
    "Entra PIM",
    "Azure Key Vault",
    "Microsoft Sentinel",
    "Azure Monitor",
    "Azure Site Recovery",
    "Azure Logic Apps",
    "Microsoft Intune",
    "Microsoft 365",
    "Microsoft Purview",
    "Defender for Cloud Apps",
    "Microsoft Defender for Cloud",
    "Microsoft Defender for Endpoint",
    "Microsoft Secure Score",
    "Microsoft Teams",
    "SharePoint",
    "OneDrive",
    "Exchange Online",
    "Microsoft Cloud PKI",
    "BitLocker",
    "Workday",
    "OneTrust",
    "FlexEra",
    "Halo (ITSM)",
    "Binary Defense",
    "BizTalk",
    "ESXi",
    "metacompliance.com",
]


def strip_numbering(text: str) -> str:
    """Strip a single leading numbering prefix; do not recurse."""
    for pattern in NUMBERING_PATTERNS:
        m = pattern.match(text)
        if m:
            return text[m.end():]
    return text


def iter_markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = REPO_ROOT / p
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            for f in path.rglob("*.md"):
                files.append(f)
    # Exclude the generated docs/ artefacts (build-portal.py output); they are
    # not hand-authored prose and are kept in sync by their own --check gate.
    return sorted(
        f for f in set(files)
        if f.relative_to(REPO_ROOT).as_posix() not in GENERATED_DOCS
    )


def check_file(path: Path) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    relative = path.relative_to(REPO_ROOT).as_posix()
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

        for m in ISE_PATTERN.finditer(line):
            findings.append(("ise", lineno, m.group(0)))

        # Skip the specs', the AI ingestion instruction's, and the document review
        # record template's own self-referential rule statements about "ensure that".
        if (not is_ingestion_spec and not is_master_spec and not is_instruction_file
                and not is_review_record_template and not is_worked_example
                and ENSURE_PATTERN.search(line)):
            findings.append(("ensure", lineno, line.strip()))

        if not is_ingestion_spec and not is_worked_example:
            for term in SANITISATION_TERMS:
                if term in line:
                    findings.append(("sanitisation", lineno, term))

        heading = HEADING_PATTERN.match(line)
        if heading and not is_worked_example:
            _, heading_text = heading.groups()
            stem = strip_numbering(heading_text)
            if stem and stem[0].islower():
                # Allow canonical lowercase project names as first word.
                first_word = re.split(r"\s|[^A-Za-z0-9_-]", stem, 1)[0].lower()
                if first_word not in LOWERCASE_PROJECT_NAMES:
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


def check_generator_source(path: Path) -> list[tuple[str, int, str]]:
    """Scan a build-*.py generator's non-docstring string literals.

    Runs the three prose house-style rules (dash, -ise, ensure that) over
    every string-constant literal that is not a docstring. The markdown-only
    checks (heading-case, sanitisation-terms) are not applied: generators
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
        for m in ISE_PATTERN.finditer(value):
            findings.append(("ise", lineno, m.group(0)))
        if ENSURE_PATTERN.search(value):
            findings.append(("ensure", lineno, value.strip()[:160]))
    return findings


def main(argv: list[str]) -> int:
    explicit = argv[1:]
    if explicit:
        md_input = explicit
        gen_input = explicit
    else:
        md_input = [
            "README.md",
            "NOTICE.md",
            "specification-master-project.md",
            "specification-ingestion.md",
            "instruction-ai-document-ingestion.md",
            # Domain run splatted from lint_common (scan-scope parity gate
            # forbids hardcoding the run).
            *AUDITED_DOMAIN_DIRS,
            # Authored adopter-facing guides; the two generated artefacts in
            # docs/ are filtered out in iter_markdown_files (see GENERATED_DOCS).
            "docs",
        ]
        gen_input = list(GENERATOR_SOURCES)

    files = iter_markdown_files(md_input)
    # Generator sources are scanned for the emitted-prose house-style rules;
    # routed by suffix so an explicit .py argument (a regression fixture) is
    # checked here while an explicit .md argument is checked as markdown.
    gen_files = [
        f for f in sorted({(REPO_ROOT / p) for p in gen_input if (REPO_ROOT / p).suffix == ".py"})
        if f.is_file()
    ]

    grouped: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f):
            grouped[f.relative_to(REPO_ROOT).as_posix()].append(finding)
            total += 1
    for f in gen_files:
        for finding in check_generator_source(f):
            grouped[f.relative_to(REPO_ROOT).as_posix()].append(finding)
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
