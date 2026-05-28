#!/usr/bin/env python3
"""Lint that file names align with Document Title fields.

For every active markdown file with a metadata block, verify that the
filename (after the doctype prefix) and the Document Title share a
recognisable common stem.

Rules:

1. The filename has the form ``<doctype>-<kebab-case-name>.md`` where
   ``<doctype>`` is one of the canonical library doctypes.
2. The Document Title is a human-readable string.
3. The two should share the same content words after normalisation
   (lowercasing, removing the doctype, removing common short words,
   converting kebab-case to space-separated, removing acronym hyphens).

This linter is permissive: it flags only clear mismatches where the
filename and the title have **no** shared significant content words.
It does not require a strict 1:1 correspondence.

The canonical use case is to catch typos and copy-paste mistakes such
as "AEO-S IT and Cybersecurity Security Requirements" where the
filename was ``annex-aeo-s-it-cybersecurity-requirements.md`` (the
duplicate "Security" in the title was a manual editing mistake).

Usage::

    python3 tools/lint-filename-title-alignment.py
    python3 tools/lint-filename-title-alignment.py --paths governance ai

Exit codes:

    0   no findings
    1   one or more findings present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXEMPT_DIRECTORY_PREFIXES: tuple[str, ...] = (
    "dev-security/claude-rules/",
    "tools/",
    "docs/",
)

EXEMPT_FILES: set[str] = {
    # Files exempt from the alignment rule. Add with a brief reason.
}

# README files and the repository root meta-files are exempt.
EXEMPT_FILENAMES: set[str] = {
    "README.md",
}

DEFAULT_PATHS = [
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "security",
    "supply-chain",
]

DOCTYPES = {
    "annex", "charter", "checklist", "framework", "guide", "guideline",
    "matrix", "plan", "policy", "procedure", "register", "roadmap",
    "sop", "specification", "standard", "template",
}

# Common short words and connectors to strip when comparing.
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "for", "to", "in", "on",
    "with", "by", "at", "as", "from", "into",
}

# Tokens that mean the same thing across filename and title variations.
# Lowercase only. The right-hand side is the canonical expansion; the linter
# treats either side of the synonym as matching if either appears in the
# opposing token set. Add new entries when the linter false-positives on a
# legitimate acronym-in-filename / expansion-in-title pattern.
SYNONYMS: dict[str, str] = {
    "kpis": "kpi",
    "kpi": "kpi",
    "uk": "united kingdom",
    "us": "united states",
    "eu": "european union",
    "sbom": "software bill of materials",
    "capa": "corrective and preventive action",
    "sox": "sarbanes oxley",
    "fedramp": "federal risk and authorization management program",
    "itgc": "it general controls",
    "aeo": "authorised economic operator",
    "ctpat": "customs trade partnership against terrorism",
    "pip": "partners in protection",
    "basc": "business alliance for secure commerce",
    "dora": "digital operational resilience act",
    "nis": "network and information systems",
    "dsar": "data subject access request",
    "ai": "artificial intelligence",
}

TITLE_PATTERN = re.compile(
    r"^\*\*Document Title:\*\*\s+(.+?)\s*$",
    re.MULTILINE,
)


def iter_active_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        full = REPO_ROOT / p
        if full.is_file() and full.suffix == ".md":
            files.append(full)
        elif full.is_dir():
            for f in full.rglob("*.md"):
                files.append(f)
    out: list[Path] = []
    for f in files:
        rel = f.relative_to(REPO_ROOT).as_posix()
        if any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES):
            continue
        if rel in EXEMPT_FILES:
            continue
        if f.name in EXEMPT_FILENAMES:
            continue
        out.append(f)
    return sorted(set(out))


def parse_title(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    m = TITLE_PATTERN.search(text)
    if not m:
        return None
    return m.group(1).strip()


def normalise_tokens(text: str) -> set[str]:
    """Tokenise text into a set of normalised content words.

    Steps:
        - lowercase
        - replace hyphens with spaces
        - strip non-alphanumeric
        - split into words
        - drop stopwords
        - expand synonyms
    """
    s = text.lower()
    s = re.sub(r"-", " ", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    tokens = s.split()
    out: set[str] = set()
    for t in tokens:
        if t in STOPWORDS:
            continue
        if len(t) <= 1:
            continue
        expanded = SYNONYMS.get(t, t)
        for piece in expanded.split():
            out.add(piece)
    return out


def filename_stem_after_doctype(filename: str) -> str | None:
    """Return the kebab-case stem of the filename after the doctype prefix.

    Returns None if the filename does not start with a known doctype prefix.
    """
    if not filename.endswith(".md"):
        return None
    name = filename[:-3]
    if "-" not in name:
        return None
    prefix, _, rest = name.partition("-")
    if prefix not in DOCTYPES:
        return None
    return rest


def check_file(path: Path) -> tuple[str, set[str], set[str]] | None:
    """Return (title, filename-tokens, title-tokens) or None if not applicable."""
    title = parse_title(path)
    if title is None:
        return None
    stem = filename_stem_after_doctype(path.name)
    if stem is None:
        return None
    fname_tokens = normalise_tokens(stem)
    title_tokens = normalise_tokens(title)
    if not fname_tokens or not title_tokens:
        return None
    return title, fname_tokens, title_tokens


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paths",
        nargs="+",
        default=DEFAULT_PATHS,
        help="Paths to scan (default: all active library directories)",
    )
    parser.add_argument(
        "--min-overlap",
        type=int,
        default=1,
        help=(
            "Minimum number of shared significant tokens required. "
            "Default 1: flag only files with zero shared tokens."
        ),
    )
    args = parser.parse_args()

    files = iter_active_files(args.paths)
    findings: list[tuple[str, str, set[str], set[str]]] = []

    for f in files:
        result = check_file(f)
        if result is None:
            continue
        title, fname_tokens, title_tokens = result
        overlap = fname_tokens & title_tokens
        if len(overlap) < args.min_overlap:
            rel = f.relative_to(REPO_ROOT).as_posix()
            findings.append((rel, title, fname_tokens, title_tokens))

    if not findings:
        print(f"OK: no filename/title alignment findings (checked {len(files)} files).")
        return 0

    for rel, title, fname_tokens, title_tokens in sorted(findings):
        print(f"=== {rel} ===")
        print(f"  title: {title}")
        print(f"  filename tokens: {sorted(fname_tokens)}")
        print(f"  title tokens:    {sorted(title_tokens)}")
        print(f"  shared:          {sorted(fname_tokens & title_tokens) or '(none)'}")

    print()
    print(f"FAIL: {len(findings)} filename/title alignment finding(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
