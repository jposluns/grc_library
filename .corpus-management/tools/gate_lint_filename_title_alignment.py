#!/usr/bin/env python3
"""Filename / Document-Title alignment audit (grc gate): pack-owned engine (source of record).

Flag a document whose filename stem (after its document-type prefix) shares no significant
content word with its ``**Document Title:**`` field. Both sides are tokenized (lowercased,
hyphens to spaces, non-alphanumerics dropped, stopwords removed, one-character tokens
dropped, synonyms expanded); a document is flagged when the overlap of the two token sets is
below a minimum (default 1, i.e. flag only zero-overlap files). A document with no title
field, or whose filename does not start with a known document-type prefix, or whose either
token set is empty, is not applicable and not flagged.

Engine/wrapper split (compile PR-18): this engine carries the PURE check (the title-field
pattern, the stopword set, ``parse_title``, ``normalise_tokens``, ``filename_stem_after_doctype``,
``check_file``) and a ``run`` that computes the overlap + reports; the project wrapper
(``tools/lint-filename-title-alignment.py``) supplies the scan scope, the grc document-type
prefix set (``DOCTYPES`` -- which must ALSO stay a module attribute of the wrapper because the
doctype-parity gate reads it there), the grc synonym map, and the minimum-overlap threshold,
passing the synonyms, doctypes, and threshold in. This engine holds no scan-scope, doctype, or
synonym policy.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

# Common short words and connectors to strip when comparing (generic).
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "for", "to", "in", "on",
    "with", "by", "at", "as", "from", "into",
}

TITLE_PATTERN = re.compile(
    r"^\*\*Document Title:\*\*\s+(.+?)\s*$",
    re.MULTILINE,
)


def parse_title(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    m = TITLE_PATTERN.search(text)
    if not m:
        return None
    title = m.group(1).strip()
    # Strip CommonMark hard-line-break backslash if present.
    if title.endswith("\\"):
        title = title[:-1].rstrip()
    return title


def normalise_tokens(text: str, synonyms: dict[str, str]) -> set[str]:
    """Tokenize text into a set of normalized content words.

    Steps: lowercase; hyphens to spaces; strip non-alphanumeric; split; drop
    stopwords and one-character tokens; expand synonyms.
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
        expanded = synonyms.get(t, t)
        for piece in expanded.split():
            out.add(piece)
    return out


def filename_stem_after_doctype(filename: str, doctypes: set[str]) -> str | None:
    """Return the kebab-case stem of the filename after the doctype prefix.

    Returns None if the filename does not start with a known doctype prefix.
    """
    if not filename.endswith(".md"):
        return None
    name = filename[:-3]
    if "-" not in name:
        return None
    prefix, _, rest = name.partition("-")
    if prefix not in doctypes:
        return None
    return rest


def check_file(
    path: Path, *, synonyms: dict[str, str], doctypes: set[str]
) -> tuple[str, set[str], set[str]] | None:
    """Return (title, filename-tokens, title-tokens) or None if not applicable."""
    title = parse_title(path)
    if title is None:
        return None
    stem = filename_stem_after_doctype(path.name, doctypes)
    if stem is None:
        return None
    fname_tokens = normalise_tokens(stem, synonyms)
    title_tokens = normalise_tokens(title, synonyms)
    if not fname_tokens or not title_tokens:
        return None
    return title, fname_tokens, title_tokens


def run(
    files: list[Path],
    *,
    synonyms: dict[str, str],
    doctypes: set[str],
    min_overlap: int,
    repo_root: Path,
) -> int:
    findings: list[tuple[str, str, set[str], set[str]]] = []
    for f in files:
        result = check_file(f, synonyms=synonyms, doctypes=doctypes)
        if result is None:
            continue
        title, fname_tokens, title_tokens = result
        overlap = fname_tokens & title_tokens
        if len(overlap) < min_overlap:
            rel = f.relative_to(repo_root).as_posix()
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
