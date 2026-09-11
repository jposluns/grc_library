#!/usr/bin/env python3
"""GRC compliance-matrix / alignment-table CCM range-direction audit.

A framework-alignment "family range" citation (for example ``CCC-01 to 09``,
``LOG-01 through LOG-14``, ``I&S-01 through I&S-09``) expresses broad CONTROL-FAMILY
coverage; the family-range convention (compliance-matrix preamble) says a range does
NOT assert every member individually applies. But a range silently SWEEPS IN each of
its members, and a member whose held CSA CCM v4.1.0 specification imposes a cloud
PROVIDER's duty toward its service customers / tenants (a "provider-to-tenant" control)
does NOT fit an INTERNAL-scope organizational document, where the organization is the
cloud CUSTOMER. Every corpus document is internal-scope (none is a CSP offering).

This is the guard-input-soundness class (AIQT ``guard-input-soundness`` /
``completeness-claim-enumerates-its-set``, adopted via the guardrails pack): a
literal-token grep over a citation is structurally BLIND to a member expressed only as
a range ENDPOINT ("CCC-01 to CCC-09" contains no "CCC-05" token), so "is a
provider-to-tenant member cited here?" must be a range-MEMBERSHIP scan
(start <= member <= end), never a token count. This gate mechanizes that scan.

Provenance: the CSA-CCM-domain-specific instance guardrails-orch directed grc to build
grc-LOCAL (intake seeds/grc-range-membership-20260908), resting on the generic AIQT
principle as the WHY. Origin incident: PRs #2081/#2082 (P-1.60 CCM-Hybrid), where a
literal-token "residual = 0" check missed CCC-05/LOG-08/I&S-06 hiding inside ranges.

Scope: DISCRETE cells (a provider-to-tenant control cited on its own, e.g. the genuine
multi-tenant container row's I&S-06) are OUT of scope here (the existence gates + the
matrix-fit cadence own that judgement); this gate checks RANGE citations only.

Exit: 0 = no swept provider-to-tenant member in any range (or all exempt); 1 = at least
one flagged; 2 = an unexpected internal error. An individually-undecodable file is
skipped (it carries no citation to check), not treated as an error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import (
    DEFAULT_EXEMPT_DIRS,
    REPO_ROOT,
    iter_markdown_targets,
    read_text_safe,
)

DIRECTIONAL_PROVIDER_MEMBERS: frozenset[str] = frozenset(
    {"I&S-06", "CCC-05", "LOG-08", "STA-04", "DSP-18", "CEK-08", "IAM-11", "IPY-02"}
)

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


def scan_targets(roots: list[Path] | None = None) -> list[Path]:
    """The gate's file-discovery scope: corpus Markdown, exempting the shared
    exempt dirs plus the ``guardrails/`` pack and ``CHANGELOG.md``. Exposed as a
    module function so the scan-scope regression can model the real scope."""
    root = Path(REPO_ROOT)
    scan_roots = roots or [root]
    return list(
        iter_markdown_targets(
            scan_roots,
            exempt_dirs=frozenset(DEFAULT_EXEMPT_DIRS) | {"guardrails"},
            exempt_files=("CHANGELOG.md",),
        )
    )


def main(argv: list[str]) -> int:
    root = Path(REPO_ROOT)
    scan_roots = [Path(p).resolve() for p in argv[1:]] or [root]
    all_findings: list[str] = []
    try:
        for path in scan_targets(scan_roots):
            text = read_text_safe(path)
            if text is None:
                continue
            rel = str(path.relative_to(root))
            all_findings.extend(scan_text(rel, text))
    except Exception as exc:  # top-level guard: any internal error -> exit 2 (the contract)
        print(f"ERROR: internal error during CCM range-direction scan: {exc}", file=sys.stderr)
        return 2
    if all_findings:
        print(
            "FAIL: CCM family-range citation(s) sweep in a provider-to-tenant "
            "member on an internal-scope document:",
            file=sys.stderr,
        )
        for f in all_findings:
            print(f"  {f}", file=sys.stderr)
        return 1
    print(
        "OK: no CCM family-range citation sweeps in any of the "
        f"{len(DIRECTIONAL_PROVIDER_MEMBERS)} tracked provider-to-tenant control members "
        "on an internal-scope document (checked by range-membership, not token grep; "
        "the tracked set is the known directional members and is extended as new ones surface)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
