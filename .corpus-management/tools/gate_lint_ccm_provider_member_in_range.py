#!/usr/bin/env python3
"""CCM family-range provider-to-tenant member direction - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(RANGE_RE, swept_members, the fence/inline-code regexes, and scan_text) is the
source of record here in the pack, moved verbatim from the grc gate. The set of
directional provider-to-tenant control members is supplied by the adopter via
configure(directional_members), so the engine carries no project catalogue; the
grc wrapper (tools/lint-ccm-provider-member-in-range.py) supplies
DIRECTIONAL_PROVIDER_MEMBERS, configures the engine, and keeps the scan scope
(scan_targets), a module-global scan_text shim, main, and the exit codes.
"""

from __future__ import annotations

import re

# The directional provider-to-tenant member set: populated by configure().
# Placeholder until an adopter calls configure(); the grc wrapper does so at import.
DIRECTIONAL_PROVIDER_MEMBERS: frozenset = frozenset()


def configure(directional_members) -> None:
    """Populate the directional provider-to-tenant member set (verbatim policy from
    the adopter). scan_text below resolves it as a module global; call once before scan_text()."""
    global DIRECTIONAL_PROVIDER_MEMBERS
    DIRECTIONAL_PROVIDER_MEMBERS = directional_members


RANGE_RE = re.compile(
    r"\b([A-Z][A-Z&]*)-(\d{1,2})\s+(?:to|through)\s+(?:([A-Z][A-Z&]*)-)?(\d{1,2})\b"
)


def swept_members(fam: str, start: int, end: int) -> list[str]:
    if end < start or (end - start) > 40:
        return []
    return [f"{fam}-{n:02d}" for n in range(start, end + 1)]


# A marker-aware fence scan (the helper pair of gate_lint_directional_dependency): the open fence is
# tracked as (character, run length), and only a same-character run at least as long, with no info
# string, closes it, so a ``` line inside a ```` or ~~~ block is content, not a toggle (3b52: a
# boolean toggle skipped a citation lying between two four-backtick blocks that each held a ``` line).
# FAIL CLOSED on block structure (maintainer ruling 2026-09-24, 3b52): fenced code blocks are NOT
# skipped, so no Markdown block structure (a fence, a list container, indentation) can hide an
# active citation; a range written as an example inside a fence is flagged, and the author writes
# it as a blockquote line or an inline code span instead. Four QA rounds showed that modelling
# CommonMark block structure by hand is an open-ended class, and the fail-closed rule costs zero
# findings on the live corpus. Inline code spans ARE skipped, by the spec's own line-local rule.


def _strip_code_spans(line: str) -> str:
    """Remove inline code spans per CommonMark: a backtick run opens a span only when a later run
    of exactly the same length closes it; a backslash-escaped backtick is literal; an unmatched
    run is literal text."""
    out, i, n = [], 0, len(line)
    while i < n:
        c = line[i]
        if c == "\\" and i + 1 < n:
            out.append(line[i:i + 2])
            i += 2
            continue
        if c != "`":
            out.append(c)
            i += 1
            continue
        j = i
        while j < n and line[j] == "`":
            j += 1
        run, k, close_end = j - i, j, None
        while k < n:
            if line[k] != "`":
                k += 1
                continue
            m = k
            while m < n and line[m] == "`":
                m += 1
            if m - k == run:
                close_end = m
                break
            k = m
        if close_end is None:
            out.append(line[i:j])
            i = j
        else:
            out.append(" ")
            i = close_end
    return "".join(out)


def scan_text(rel: str, text: str) -> list[str]:
    findings: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        # A blockquote line is an example / quotation, not an active citation.
        if line.lstrip().startswith(">"):
            continue
        # Strip inline-code spans so a range shown as `CCC-01 to 09` is not flagged.
        scanned = _strip_code_spans(line)
        for m in RANGE_RE.finditer(scanned):
            fam, start_s, fam2, end_s = m.group(1), m.group(2), m.group(3), m.group(4)
            # A mixed-family range (e.g. "CCC-01 to LOG-09") is malformed, not a
            # single-family citation; do not infer the first family across it.
            if fam2 is not None and fam2 != fam:
                continue
            members = swept_members(fam, int(start_s), int(end_s))
            hit = [c for c in members if c in DIRECTIONAL_PROVIDER_MEMBERS]
            if hit:
                findings.append(
                    f"{rel}:{i}: family range `{m.group(0)}` sweeps in "
                    f"provider-to-tenant member(s) {', '.join(hit)} on an "
                    f"internal-scope document; split the range to exclude them "
                    f"(see the family-range convention)."
                )
    return findings

