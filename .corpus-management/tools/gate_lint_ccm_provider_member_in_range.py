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


FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def scan_text(rel: str, text: str) -> list[str]:
    findings: list[str] = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # A blockquote line is an example / quotation, not an active citation.
        if line.lstrip().startswith(">"):
            continue
        # Strip inline-code spans so a range shown as `CCC-01 to 09` is not flagged.
        scanned = INLINE_CODE_RE.sub("", line)
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

