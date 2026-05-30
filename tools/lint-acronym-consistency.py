#!/usr/bin/env python3
"""Verify acronym definitions across the library against the glossary.

The library uses [`governance/register-glossary.md`](register-glossary.md) as the
single source of truth for acronym expansions. Inline definitions of the
form "Expansion (ACRONYM)" must match what the glossary records.

This linter:
- Parses the glossary register into an acronym -> expansion map.
- Walks every artefact document looking for inline acronym definitions
  of the form "Expansion (ACRONYM)" where ACRONYM is 2-6 uppercase
  letters or letters+digits.
- Flags definitions whose expansion phrase materially diverges from
  the glossary.

The linter is conservative: it flags only cases where the inline
expansion's main content words do not overlap with the glossary's
expansion content words. Stylistic differences (a/the/of) are tolerated.

Acronyms not in the glossary are not flagged by this linter (a separate
"glossary coverage" linter would catch those; this one focuses on
expansion consistency).

Usage:
    python3 tools/lint-acronym-consistency.py
    python3 tools/lint-acronym-consistency.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more acronym expansion inconsistencies present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = [str(REPO_ROOT)]

GLOSSARY = REPO_ROOT / "governance" / "register-glossary.md"

# Glossary entry: | **ACRONYM** | Expansion. ... |
GLOSSARY_ROW_RE = re.compile(r"^\|\s*\*\*([A-Z][A-Z0-9\-./]{1,8})\*\*\s*\|\s*(.+?)\s*\|", re.MULTILINE)

# Inline acronym definition: "Some Words Or Phrase (ACRONYM)"
# Require the acronym to be 2-6 uppercase letters / digits / hyphens,
# preceded by at least one capitalized expansion word.
INLINE_DEF_RE = re.compile(
    r"\b((?:[A-Z][A-Za-z0-9'\-]+\s+){1,8}[A-Z][A-Za-z0-9'\-]+)\s+\(([A-Z][A-Z0-9\-]{1,5})\)"
)

# Stopwords to ignore when comparing expansions
STOPWORDS = {
    "a", "an", "and", "or", "of", "for", "the", "in", "on", "to",
    "by", "with", "at", "from", "into", "via", "per", "as",
}

EXEMPT_DIR_PARTS = {".git", "node_modules", "__pycache__"}

EXEMPT_FILES = {
    # The glossary itself; the linter source.
    "register-glossary.md",
    "lint-acronym-consistency.py",
    # The CHANGELOG describes the patterns and is allowed to use them freely.
    "CHANGELOG.md",
}


def parse_glossary() -> dict[str, set[str]]:
    """Return acronym -> set of significant words in its glossary expansion."""
    out: dict[str, set[str]] = {}
    if not GLOSSARY.exists():
        return out
    text = GLOSSARY.read_text(encoding="utf-8")
    for m in GLOSSARY_ROW_RE.finditer(text):
        acr = m.group(1)
        # Use the whole expansion cell (including parenthetical alternate
        # expansions) so the linter accepts overloaded acronyms.
        expansion = m.group(2)
        # Strip markdown formatting
        expansion = re.sub(r"\*+", "", expansion)
        tokens = re.findall(r"[A-Za-z][A-Za-z0-9'\-]*", expansion.lower())
        sig = {t for t in tokens if t not in STOPWORDS and len(t) > 1}
        if acr in out:
            out[acr] |= sig
        else:
            out[acr] = sig
    return out


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in EXEMPT_FILES:
        return False
    return True


def scan(path: Path, glossary: dict[str, set[str]]) -> list[tuple[int, str, str, str]]:
    findings: list[tuple[int, str, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in INLINE_DEF_RE.finditer(line):
            expansion_phrase = m.group(1)
            acr = m.group(2)
            if acr not in glossary:
                continue
            inline_sig = {
                t for t in re.findall(r"[A-Za-z][A-Za-z0-9'\-]*", expansion_phrase.lower())
                if t not in STOPWORDS and len(t) > 1
            }
            glossary_sig = glossary[acr]
            if not inline_sig or not glossary_sig:
                continue
            # If at least one significant word overlaps, accept.
            if inline_sig & glossary_sig:
                continue
            findings.append(
                (
                    lineno,
                    acr,
                    expansion_phrase,
                    f"inline expansion words {sorted(inline_sig)} do not overlap glossary words {sorted(glossary_sig)}",
                )
            )
    return findings


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Verify acronym expansion consistency against the glossary."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    glossary = parse_glossary()
    if not glossary:
        print("OK: no glossary entries found; nothing to check.")
        return 0
    targets = iter_targets(args.paths)
    grouped: dict[Path, list[tuple[int, str, str, str]]] = {}
    for t in targets:
        findings = scan(t, glossary)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all inline acronym expansions match the glossary (scanned {len(targets)} files; {len(glossary)} glossary entries).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, acr, phrase, msg in findings:
            print(f"  L{lineno} [acronym-inconsistency] {acr}: {phrase!r} - {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} acronym-consistency finding(s) across {len(grouped)} file(s).")
    print(
        "Inline acronym expansions should be consistent with the glossary "
        "(governance/register-glossary.md). Either match the glossary expansion or "
        "update the glossary if the inline definition is more current."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
