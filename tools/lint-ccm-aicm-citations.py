#!/usr/bin/env python3
"""CSA CCM / AICM citation-accuracy audit.

The corpus cites CSA Cloud Controls Matrix (CCM v4.1.0) and AI Controls
Matrix (AICM v1.1.0) control identifiers throughout its framework-alignment
tables, registers, and prose. Two recurring failure modes are not caught by
the generic citation gate (``lint-citations.py``):

  1. **Invalid / superseded domain codes.** Citing a domain that does not
     exist in the current matrices (e.g. ``GOV`` -- there is no GOV domain;
     governance is ``GRC``), a superseded code (``IVS`` was renamed to
     ``I&S`` in CCM v4.1.0; ``GRM`` was the v3.0.1 governance code), a
     fabricated domain (``NET`` -- network controls live in ``I&S``), or a
     control number beyond the domain's range (``IPY-05`` -- the IPY domain
     has only four controls). This whole class was found across ~9 documents
     and corrected in the PR that introduced this gate.

  2. **Mis-attributed control titles.** A control-listing row that names a
     valid code but gives it a title belonging to a different (or invented)
     control -- e.g. an ``MDS-01`` row titled "Model Inventory" when the
     authoritative AICM v1.1.0 ``MDS-01`` is "Training Pipeline Security".

The authoritative reference (domain codes, control-ID ranges, and canonical
control titles) lives in :mod:`ccm_aicm_reference`, a fair-use citation index
derived from the CSA-published catalogues (see that module's provenance note;
the full matrices are not redistributed).

Checks:

  * **Code validity** (corpus-wide): every ``<DOMAIN>-<NN>`` token whose
    DOMAIN is a CCM/AICM-family prefix (a valid domain OR a known-bad one)
    is validated. A known-bad domain fails with the correct code; a valid
    domain with an out-of-range number fails. Tokens preceded by a letter,
    digit, or hyphen (the corpus-internal ``MODEL-GOV-01`` / ``AI-GOV-01``
    identifiers) are NOT policed -- they are not CCM citations.

  * **Title match** (control-listing tables only): a markdown row of the
    shape ``| <CODE> | <title> | ...`` whose CODE is a known control is
    checked against the canonical title. To tolerate the corpus's localized
    and abbreviated titles (Canadian/Commonwealth spelling, shortened
    forms), the check is deliberately conservative: it fails ONLY when the
    cited title shares NO significant content word with the canonical title
    (the fabricated-title signal), never on a mere wording difference.

Scope: ``*.md`` under the repository root, minus DEFAULT_EXEMPT_DIRS (which
includes ``.working`` and ``.claude``) and the append-only CHANGELOG files.

Exit codes: 0 pass, 1 findings, 2 internal error (reference unavailable).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from lint_common import (
    DEFAULT_EXEMPT_DIRS,
    REPO_ROOT,
    iter_markdown_targets,
    read_text_safe,
)

try:
    from ccm_aicm_reference import ALL_TITLES, KNOWN_BAD_DOMAINS, VALID_DOMAINS
except ImportError as exc:  # pragma: no cover - import guard
    print(f"ERROR: cannot load ccm_aicm_reference: {exc}", file=sys.stderr)
    sys.exit(2)

# Meta-documents whose purpose is to describe this gate's rule set inevitably
# contain the codes the gate searches for; per the audit-programme spec §3.4
# (design principle 4, meta-document exception) they are exempted by name.
# CHANGELOG.md (and its .working detailed mirror) carry historical examples;
# the audit-programme and citation-verification specs document the gate itself.
EXEMPT_FILES = frozenset({
    "CHANGELOG.md",
    "specification-audit-programme.md",
    "specification-citation-verification.md",
})

# CCM/AICM-family domain prefixes worth policing: the valid domains plus the
# historically-seen wrong ones. A token whose prefix is outside this set (an
# ISO clause, a NIST 800-53 control like ``AC-2``, a CSF code) is ignored, so
# the gate does not false-positive on other frameworks' identifiers.
CCM_FAMILY = frozenset(VALID_DOMAINS) | frozenset(KNOWN_BAD_DOMAINS)

# A CCM/AICM control token: DOMAIN-NN, not preceded by a letter/digit/hyphen
# (so MODEL-GOV-01 and AI-GOV-01 are excluded) and not followed by a digit
# (so ISO-27001 and three-digit numbers do not match).
CODE_RE = re.compile(r"(?<![A-Za-z0-9-])([A-Z&]{2,5})-(\d{1,2})(?![0-9])")

# A control-listing table row: first cell a bare code, second cell the title.
ROW_RE = re.compile(r"^\|\s*([A-Z&]{2,5}-\d{1,2})\s*\|\s*([^|]*?)\s*\|")

_STOPWORDS = frozenset(
    {"and", "the", "of", "for", "to", "in", "on", "by", "with", "or",
     "a", "an", "&", "is", "as", "at"}
)


def _content_words(title: str) -> set[str]:
    toks = re.split(r"[^A-Za-z0-9]+", title.lower())
    return {t for t in toks if len(t) >= 2 and t not in _STOPWORDS}


@dataclass
class Finding:
    path: Path
    line: int
    rule: str
    message: str
    text: str


def scan_file(path: Path) -> list[Finding]:
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Check 1: code validity.
        for m in CODE_RE.finditer(line):
            domain, num = m.group(1), int(m.group(2))
            if domain not in CCM_FAMILY:
                continue
            if domain in KNOWN_BAD_DOMAINS:
                findings.append(Finding(
                    path, i, "invalid-ccm-domain",
                    f"'{m.group(0)}' uses '{domain}', not a CCM v4.1 / AICM "
                    f"v1.1 domain code; use {KNOWN_BAD_DOMAINS[domain]}",
                    line.strip()[:140]))
            elif num > VALID_DOMAINS[domain]:
                findings.append(Finding(
                    path, i, "ccm-control-out-of-range",
                    f"'{m.group(0)}' exceeds the {domain} domain's range "
                    f"({domain}-01..{domain}-{VALID_DOMAINS[domain]:02d})",
                    line.strip()[:140]))

        # Check 2: title match on control-listing rows.
        rm = ROW_RE.match(line)
        if rm:
            code, title = rm.group(1), rm.group(2).strip()
            canonical = ALL_TITLES.get(code)
            if canonical and title and title.lower() != "control title":
                if not (_content_words(title) & _content_words(canonical)):
                    findings.append(Finding(
                        path, i, "ccm-title-mismatch",
                        f"'{code}' titled '{title}' shares no content word "
                        f"with the catalogue title '{canonical}'",
                        line.strip()[:140]))
    return findings


def main(argv: list[str]) -> int:
    paths = argv[1:] or [str(REPO_ROOT)]
    targets = iter_markdown_targets(
        paths, exempt_dirs=DEFAULT_EXEMPT_DIRS, exempt_files=EXEMPT_FILES)
    all_findings: list[Finding] = []
    for path in targets:
        all_findings.extend(scan_file(path))

    if not all_findings:
        print(
            f"OK: CCM/AICM citations valid across {len(targets)} files "
            f"({len(VALID_DOMAINS)} domains, {len(ALL_TITLES)} controls in the "
            f"CCM v4.1.0 / AICM v1.1.0 reference).")
        return 0

    by_file: dict[Path, list[Finding]] = {}
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
