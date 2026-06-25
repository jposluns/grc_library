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

Usage:
    python3 tools/lint-language.py [paths...]

Exits non-zero if any findings are reported.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from lint_common import iter_non_code_lines, read_text_safe

REPO_ROOT = Path(__file__).resolve().parent.parent
INGESTION_SPEC = "specification-ingestion.md"

ISE_PATTERN = re.compile(
    r"\b("
    r"recognise|recognised|recognising|"
    r"organise|organised|organising|"
    r"prioritise|prioritised|prioritising|"
    r"categorise|categorised|categorising|"
    r"emphasise|emphasised|emphasising|"
    r"harmonise|harmonised|harmonising|"
    r"standardise|standardised|standardising|"
    r"optimise|optimised|optimising|"
    r"centralise|centralised|centralising|"
    r"customise|customised|customising|"
    r"finalise|finalised|finalising|"
    r"specialise|specialised|specialising|"
    r"utilise|utilised|utilising|"
    r"minimise|minimised|minimising|"
    r"maximise|maximised|maximising|"
    r"criticise|criticised|criticising|"
    r"generalise|generalised|generalising|"
    r"operationalise|operationalised|operationalising"
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
    return sorted(set(files))


def check_file(path: Path) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    relative = path.relative_to(REPO_ROOT).as_posix()
    is_ingestion_spec = relative == INGESTION_SPEC
    is_master_spec = relative == "specification-master-project.md"
    is_instruction_file = relative == "instruction-ai-document-ingestion.md"
    is_review_record_template = relative == "governance/template-document-review-record.md"

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
                and not is_review_record_template
                and ENSURE_PATTERN.search(line)):
            findings.append(("ensure", lineno, line.strip()))

        if not is_ingestion_spec:
            for term in SANITISATION_TERMS:
                if term in line:
                    findings.append(("sanitisation", lineno, term))

        heading = HEADING_PATTERN.match(line)
        if heading:
            _, heading_text = heading.groups()
            stem = strip_numbering(heading_text)
            if stem and stem[0].islower():
                # Allow canonical lowercase project names as first word.
                first_word = re.split(r"\s|[^A-Za-z0-9_-]", stem, 1)[0].lower()
                if first_word not in LOWERCASE_PROJECT_NAMES:
                    findings.append(("heading-case", lineno, line.strip()))

    return findings


def main(argv: list[str]) -> int:
    paths = argv[1:] or [
        "README.md",
        "NOTICE.md",
        "specification-master-project.md",
        "specification-ingestion.md",
        "instruction-ai-document-ingestion.md",
        "ai",
        "architecture",
        "compliance",
        "dev-security",
        "governance",
        ".project-governance",
        "operations",
        "privacy",
        "resilience",
        "risk",
        "security",
        "supply-chain",
    ]

    files = iter_markdown_files(paths)
    grouped: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f):
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
