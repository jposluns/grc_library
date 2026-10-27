#!/usr/bin/env python3
"""Per-document CSA CCM v4.1.0 / AICM v1.1.0 citation validity - grc wrapper over the pack engine.

Validate every CSA CCM v4.1.0 / AICM v1.1.0 control-code citation in the corpus
against the authoritative catalogue in :mod:`ccm_aicm_reference` (domain validity,
control-number range, per-catalogue title fit, bare-domain and bare-code checks,
and the cross-catalogue title-confusion check).

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(Finding, the token/heading/context regexes, the helpers, and scan_file) is the
source of record in the pack engine
(.corpus-management/tools/gate_lint_ccm_aicm_citations.py); it is catalogue-agnostic
and takes the reference via configure(ref). This wrapper imports the shared grc
reference catalogue, configures the engine with it, and keeps the grc scan scope
(main's iter_markdown_targets over REPO_ROOT with EXEMPT_FILES), the module-global
scan_file(path) shim, the reporting, and the exit codes.

Glossary domain-name check (3b296, wrapper-side): the "(CSA CCM domain) <Name>" row
form is a grc glossary convention, so the engine does not know it. Every row of a
scanned ``register-glossary.md`` carrying that marker must give the EXACT
DOMAIN_NAMES name for its code (strict: "and" for "&" is reported as a form
difference; another domain's name is reported as that domain). The row's code must
be a known domain (the KNOWN_BAD_DOMAINS hint is given where one exists) and, under a
CCM-only marker, a CCM domain (not AICM-only MDS). A row is flagged for equating its
domain with a different domain when a code occurs in the same phrase as a
non-negated equivalence word ("interchangeabl...", "synonym...", "alias...",
"equivalen...", "same as", or "same <noun> as"); a word counts as negated when
"not", "never", "no", "neither", "nor", "cannot" or a word ending in "n't" is
among the three words (within 80 characters) before it, and a negator further
back is not seen. Phrases end at a ";", a "." followed by whitespace or the end
of the row (the "." in "v4.1" does not end one), a "(N)", a comma, and the
contrast words "but", "whereas", "while", "unlike", "distinct from" and "not".
An equivalence spanning any of these boundaries can be missed. A sentence mixing
a positive and a negated equivalence in one phrase, or using an unlisted contrast
word ("rather than", "instead of"), can be reported as an equivalence (a loud false
positive). An in-row "CODE (Name)"
cross-mention must use the canonical name. A tree without the glossary
(an adopter fork) is skipped; a glossary with no marker rows passes. Every run also
checks that VALID_DOMAINS and DOMAIN_NAMES cover the same set of codes.
"""

from __future__ import annotations

import re
import sys
import types
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, guard_explicit_paths_cwd, is_fence_line, iter_markdown_targets, positional_args, read_text_safe, refuse_vanished, scan_listed  # noqa: E402  # grc-config/store, stays local

try:
    from ccm_aicm_reference import (  # noqa: E402  # grc reference catalogue (fair-use citation index)
        AICM_V11,
        ALL_TITLES,
        CCM_DOMAINS,
        CCM_V41,
        DOMAIN_NAMES,
        KNOWN_BAD_DOMAINS,
        VALID_DOMAINS,
    )
except ImportError as exc:  # pragma: no cover - import guard
    print(f"ERROR: cannot load ccm_aicm_reference: {exc}", file=sys.stderr)
    sys.exit(2)

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_ccm_aicm_citations  # the pack-owned engine (source of record)
    return gate_lint_ccm_aicm_citations


# Configure the engine ONCE with the grc CCM/AICM reference catalogue. The engine
# builds every derived structure (CCM_FAMILY, the bare-code/bare-domain regexes,
# DIVERGENT_CONTROLS) from this, verbatim from the original gate's module level.
_engine().configure(types.SimpleNamespace(
    VALID_DOMAINS=VALID_DOMAINS,
    KNOWN_BAD_DOMAINS=KNOWN_BAD_DOMAINS,
    CCM_V41=CCM_V41,
    AICM_V11=AICM_V11,
    ALL_TITLES=ALL_TITLES,
    DOMAIN_NAMES=DOMAIN_NAMES,
))

# Meta-documents whose purpose is to describe this gate's rule set inevitably
# contain the codes the gate searches for; they are exempted by name (kept
# wrapper-side, grc scan config).
EXEMPT_FILES = frozenset({
    "CHANGELOG.md",
    "specification-audit-programme.md",
    "specification-citation-verification.md",
    "TODO.md",
    "TODO-REFERENCE.md",
})


def scan_file(path: Path) -> list:
    """Thin shim delegating to the pack engine's pure scan.

    Kept as a module-global because a regression test may call ``mod.scan_file(path)``
    directly; the engine is already configured with the grc reference at import.
    """
    return _engine().scan_file(path)


# Glossary domain-name check (3b296). Only a file with this name is checked, so an
# adopter fork without the glossary is skipped and a fixture can stand in for it.
GLOSSARY_NAME = "register-glossary.md"
REFERENCE_PATH = Path(__file__).resolve().parent / "ccm_aicm_reference.py"

# A glossary row is split on unescaped "|" (no regex over the whole line, so a long
# malformed row costs linear time): first cell a bold term, the rest the definition.
# A "|" is escaped when an odd run of backslashes precedes it; the lookbehind starts
# each match at the beginning of a run, so a long run is scanned once.
PIPE_RE = re.compile(r"(?<!\\)(\\*)\|")
TERM_CELL_RE = re.compile(r"\*\*(?P<term>[^*]+)\*\*")
# The domain marker, tolerant of the "(CCM domain)" / "(CSA CCM/AICM domain)" variants.
DOMAIN_MARKER_RE = re.compile(r"\((?:CSA\s+)?(?:CCM|AICM)(?:\s*/\s*AICM)?\s+domain\)\s*", re.I)
# The expansion ends at the first sentence/clause break, "(2)", or next marker.
EXPANSION_END_RE = re.compile(r"[.;](?=\s|$)|\(2\)")
# A clause ends at a ";", a "." followed by whitespace or the end (not the one inside
# "v4.1") or a "(N)".
CLAUSE_SPLIT_RE = re.compile(r"[.;](?=\s|$)|\(\d+\)")
# A domain code as a bare token (same boundary as the engine's bare-domain regexes),
# built from DOMAIN_NAMES so I&S and A&A match and the set stays in sync.
_DOMAIN_TOKEN = (r"(?<![A-Za-z0-9.&\-])("
                 + "|".join(re.escape(c) for c in sorted(DOMAIN_NAMES, key=len, reverse=True))
                 + r")(?![A-Za-z0-9\-])")
DOMAIN_TOKEN_RE = re.compile(_DOMAIN_TOKEN)
# A word claiming two domains are the same ("interchangeably", "the same domain as");
# "same <noun> as" needs a naming noun, so "at the same time as" is not one.
EQUIVALENCE_RE = re.compile(
    r"\b(?:interchangeabl\w*|same(?:\s+(?:domain|code|name|acronym|abbreviation|meaning|thing))?"
    r"\s+as|synonym\w*|alias\w*|equivalen\w*)\b", re.I)
# A negator within the three words before an equivalence word cancels it. Only a
# bounded tail before the word is read, so a long clause costs linear time.
NEGATORS = frozenset({"not", "never", "no", "neither", "nor", "cannot"})
NEGATION_TAIL = 80
WORD_RE = re.compile(r"[A-Za-z'\u2019]+")  # straight or curly apostrophe
# A phrase starts after a comma or one of these contrast words.
PHRASE_BREAK_RE = re.compile(r",|\b(?:but|whereas|while|unlike|distinct\s+from|not)\b", re.I)
# An in-row cross-mention of a domain with its name, e.g. "DCS (Datacenter Security)".
CROSS_MENTION_RE = re.compile(_DOMAIN_TOKEN + r"\s+\(([^()]+)\)")


def _glossary_row(line: str) -> tuple[str, str] | None:
    """The (term, body) of a "| **TERM** | body |" row, or None for any other line."""
    if not line.startswith("|"):
        return None
    line = line.rstrip()
    cells: list = []
    start = 0
    for pm in PIPE_RE.finditer(line):
        if len(pm.group(1)) % 2 == 0:
            cells.append(line[start:pm.end() - 1])
            start = pm.end()
    cells.append(line[start:])
    if len(cells) < 4 or cells[-1]:
        return None  # no definition cell, or no closing unescaped "|"
    tm = TERM_CELL_RE.fullmatch(cells[1].strip())
    if not tm or not tm["term"].strip():
        return None
    return tm["term"].strip(), "|".join(cells[2:-1]).strip()


def _negated(clause: str, end: int) -> bool:
    """True when one of the three words before ``clause[end]`` negates what follows."""
    start = max(0, end - NEGATION_TAIL)
    # A word cut by the tail's start is dropped, so "piano" is not read as "no".
    words = [wm.group(0).lower().replace("\u2019", "'")
             for wm in WORD_RE.finditer(clause, start, end)
             if not (wm.start() == start and start and WORD_RE.match(clause, start - 1, start))][-3:]
    return any(w in NEGATORS or w.endswith("n't") for w in words)


def _equated_codes(body: str) -> list:
    """Domain codes whose own phrase holds a non-negated equivalence word."""
    codes: list = []
    for clause in CLAUSE_SPLIT_RE.split(body):
        positive = [eq.start() for eq in EQUIVALENCE_RE.finditer(clause)
                    if not _negated(clause, eq.start())]
        if not positive:
            continue
        breaks = [pb.start() for pb in PHRASE_BREAK_RE.finditer(clause)]
        break_index = 0
        positive_index = 0
        for dm in DOMAIN_TOKEN_RE.finditer(clause):
            while break_index < len(breaks) and breaks[break_index] <= dm.start():
                break_index += 1
            start = breaks[break_index - 1] if break_index else 0
            end = breaks[break_index] if break_index < len(breaks) else len(clause)
            while positive_index < len(positive) and positive[positive_index] < start:
                positive_index += 1
            if positive_index < len(positive) and positive[positive_index] < end:
                codes.append(dm.group(1))
    return codes


def _loose(name: str) -> str:
    """Loose form of a domain name: case, '&' vs 'and', commas and spacing ignored."""
    name = name.casefold().replace("&", " and ")
    name = re.sub(r",\s*and\b", " and", name)
    return re.sub(r"[\s,]+", " ", name).strip()


_LOOSE_TO_CODE = {_loose(n): c for c, n in DOMAIN_NAMES.items()}


def _name_issue(code: str, name: str) -> str | None:
    """Why ``name`` is not the exact DOMAIN_NAMES name of ``code`` (None when it is)."""
    want = DOMAIN_NAMES[code]
    if name == want:
        return None
    other = _LOOSE_TO_CODE.get(_loose(name))
    if other and other != code:
        return f"{name!r} is the name of a different domain, {other}; {code} is {want!r}"
    if _loose(name) == _loose(want):
        return f"{name!r} is a form difference from the canonical {want!r}"
    return f"{name!r} is not the canonical {want!r}"


def scan_glossary(path: Path, *, listed: bool = False) -> list:
    """Check the "(CSA CCM domain) <Name>" rows of a glossary file against DOMAIN_NAMES.

    ``listed`` (3b653): main() passes a file its walk listed, so a glossary gone
    when read raises FileNotFoundError for scan_listed to refuse, never a pass.
    """
    if not listed and not path.is_file():
        return []  # adopter fork without the glossary: nothing to check
    text = read_text_safe(path)
    if text is None:
        return []
    finding = _engine().Finding
    findings: list = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if is_fence_line(line):
            in_fence = not in_fence
            continue
        row = None if in_fence else _glossary_row(line)
        if not row or not DOMAIN_MARKER_RE.search(row[1]):
            continue
        term, body = row

        def add(rule: str, message: str) -> None:
            findings.append(finding(path, i, rule, f"{term}: {message}", line))

        markers = list(DOMAIN_MARKER_RE.finditer(body))
        expansion_ends = iter(EXPANSION_END_RE.finditer(body))
        expansion_end = next(expansion_ends, None)
        for marker_index, mk in enumerate(markers):
            if term not in DOMAIN_NAMES:
                hint = KNOWN_BAD_DOMAINS.get(term)
                add("ccm-glossary-unknown-domain", "not a CCM/AICM domain code"
                    + (f"; use {hint}" if hint else ""))
                continue
            if term not in CCM_DOMAINS and "AICM" not in mk.group(0).upper():
                add("ccm-glossary-aicm-only-domain",
                    f"AICM-only domain ({DOMAIN_NAMES[term]}) labelled as a CCM domain")
            while expansion_end and expansion_end.start() < mk.end():
                expansion_end = next(expansion_ends, None)
            end = min(expansion_end.start() if expansion_end else len(body),
                      markers[marker_index + 1].start()
                      if marker_index + 1 < len(markers) else len(body))
            issue = _name_issue(term, body[mk.end():end].strip())
            if issue:
                add("ccm-glossary-domain-name", f"domain expansion {issue}")
        for code in dict.fromkeys(_equated_codes(body)):
            if code != term:
                add("ccm-glossary-domain-equivalence",
                    f"row equates {term} with the distinct {code} domain "
                    f"({DOMAIN_NAMES[code]!r})")
        for cm in CROSS_MENTION_RE.finditer(body):
            issue = _name_issue(cm.group(1), cm.group(2).strip())
            if issue:
                add("ccm-glossary-cross-mention", f"cross-mention {cm.group(0)!r}: {issue}")
    return findings


def reference_findings() -> list:
    """Self-consistency of the reference: VALID_DOMAINS and DOMAIN_NAMES name the same codes."""
    drift = set(VALID_DOMAINS) ^ set(DOMAIN_NAMES)
    if not drift:
        return []
    text = read_text_safe(REFERENCE_PATH) or ""
    line = next((i for i, ln in enumerate(text.splitlines(), start=1)
                 if ln.startswith("DOMAIN_NAMES =")), 1)
    finding = _engine().Finding
    return [finding(REFERENCE_PATH, line, "ccm-reference-domain-drift",
                    f"{code} is in {'VALID_DOMAINS' if code in VALID_DOMAINS else 'DOMAIN_NAMES'}"
                    f" only", "") for code in sorted(drift)]


def main(argv: list[str]) -> int:
    # 3b48: explicit paths are refused when missing or outside this tree, else normalized.
    args = positional_args(argv[1:], known_flags=())  # 3b50b2c: '--' separates paths (quick-guard passes one)
    paths = guard_explicit_paths_cwd(args, repo_root=REPO_ROOT) if args else [str(REPO_ROOT)]
    targets = iter_markdown_targets(
        paths, exempt_dirs=DEFAULT_EXEMPT_DIRS, exempt_files=EXEMPT_FILES,
        skip_test_scratch=True)  # 3b653: tests/tmp fixtures vanish mid-walk
    all_findings: list = reference_findings()
    vanished: list[Path] = []
    for path in targets:
        all_findings.extend(scan_listed(lambda: scan_file(path), path, vanished))
        if path.name == GLOSSARY_NAME and path not in vanished:
            all_findings.extend(scan_listed(lambda: scan_glossary(path, listed=True), path, vanished))
    if vanished:
        return refuse_vanished(vanished)

    if not all_findings:
        print(
            f"OK: CCM/AICM citations valid across {len(targets)} files "
            f"({len(VALID_DOMAINS)} domains, {len(ALL_TITLES)} controls in the "
            f"CCM v4.1.0 / AICM v1.1.0 reference).")
        return 0

    by_file: dict = {}
    for f in all_findings:
        by_file.setdefault(f.path, []).append(f)
    for path in sorted(by_file):
        print(f"=== {path.relative_to(REPO_ROOT).as_posix()} ===")
        for f in by_file[path]:
            print(f"  L{f.line} [{f.rule}] {f.message}")
    print(
        f"\nFAIL: {len(all_findings)} CCM/AICM citation issue(s) across "
        f"{len(by_file)} file(s). The authoritative reference is "
        f"tools/ccm_aicm_reference.py (CSA CCM v4.1.0 / AICM v1.1.0).",
        file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
