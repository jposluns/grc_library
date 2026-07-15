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
    checked against the canonical title. The lookup is **section-aware**: a
    row under a ``## CSA CCM ...`` heading is checked against the CCM v4.1.0
    title, one under an ``## AICM ...`` heading against the AICM v1.1.0 title,
    and one under neither against the AICM-wins union (the prior behaviour on
    unscoped tables). To tolerate the corpus's localized and abbreviated
    titles (Canadian/Commonwealth spelling, shortened forms), the check is
    deliberately conservative: it fails ONLY when the cited title shares NO
    significant content word with the canonical title (the fabricated-title
    signal), never on a mere wording difference.

  * **Cross-catalogue title** (control-listing tables under a CCM/AICM
    section): a small set of controls share a code across both matrices but
    carry a title that differs by a distinctive content word (e.g. I&S-07 is
    "Migration to Cloud Environments" in CCM v4.1.0 but "Migration to Hosted
    Environments" in AICM v1.1.0). Because the two titles share most content
    words, the conservative content-word check above never fires on the mix-up.
    This check fails a row under a CCM section whose title carries the AICM
    variant's distinctive word (and none of the CCM variant's), and vice versa.
    Controls whose titles differ only by punctuation (IAM-11's apostrophe)
    have no distinctive content word and are intentionally not policed.

  * **Bare domain code** (CCM/CSA-context lines): a superseded or fabricated
    domain code cited as a bare token with no ``-NN`` suffix (a framework
    family list, a domain-keyed crosswalk row, a glossary-style entry) carries
    nothing for the code-validity check to see. This check flags such a bare
    known-bad code when the line either names the matrices (CCM / CSA / Cloud
    Controls Matrix / AICM) or sits under a CCM/AICM section heading, and is
    not a historical rename-note (``renamed`` / ``superseded`` / ``corrected``
    and similar). The boundary excludes ``.NET``, the corpus-internal
    ``AI-GOV`` / ``MODEL-GOV`` identifiers, and the ``<CODE>-<NN>`` tokens; the
    CCM-context requirement excludes currency ``AUD`` and "government" prose.
    Recall is deliberately precision-first: a bad code in a multi-framework
    mapping table where the CCM column is unlabelled on the row and the section
    heading is generic is not caught here (the orchestrator's apply-time
    standalone-token grep and the periodic sweep cover that tail).

  * **Framework-as-column family** (framework-alignment tables with a CSA CCM /
    AICM column): the code-validity check above policies only tokens whose
    DOMAIN prefix it *recognizes* (a valid CCM/AICM domain or a known-bad one),
    so an INVENTED family prefix that no matrix defines (``END`` -- endpoints
    are ``UEM``; ``ISM``; ``GVN`` -- governance is ``GRC``) is silently skipped
    even when cited in a column explicitly headed ``CSA CCM v4.1`` or ``AICM``.
    This check closes that blind spot (the deep-assessment r1 R11 discovery,
    PR #782): in a framework-alignment table whose header row has a cell
    matching ``CSA CCM`` / ``Cloud Controls Matrix`` / ``AICM``, every
    control-code-shaped token in that column's body cells must use a real
    CCM/AICM domain prefix; a token whose prefix is outside the CCM/AICM family
    is flagged as an unknown family. Scoped to the named column only, so a NIST
    ``AC-2`` in a NIST column or an ISO clause elsewhere is untouched, and
    known-bad domains stay with the code-validity check (no double-flag).

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
    is_fence_line,
    iter_markdown_targets,
    read_text_safe,
)

try:
    from ccm_aicm_reference import (
        AICM_V11,
        ALL_TITLES,
        CCM_V41,
        KNOWN_BAD_DOMAINS,
        VALID_DOMAINS,
    )
except ImportError as exc:  # pragma: no cover - import guard
    print(f"ERROR: cannot load ccm_aicm_reference: {exc}", file=sys.stderr)
    sys.exit(2)

# Meta-documents whose purpose is to describe this gate's rule set inevitably
# contain the codes the gate searches for; per the audit-programme spec §3.4
# (design principle 4, meta-document exception) they are exempted by name.
# CHANGELOG.md (and its .working detailed mirror) carry historical examples;
# the audit-programme and citation-verification specs document the gate itself;
# TODO.md is forward-looking backlog meta that names the superseded codes when
# describing the gate's own follow-up items (the S5 entry, DD-12, the sweep
# cursor), not corpus citation content, so the bare-domain-code check (Check 4)
# would otherwise false-positive on it.
EXEMPT_FILES = frozenset({
    "CHANGELOG.md",
    "specification-audit-programme.md",
    "specification-citation-verification.md",
    "TODO.md",
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

# A markdown heading (any level). Used to track which catalogue a control-listing
# table sits under, so a row under a "## CSA CCM ..." section is title-checked
# against the CCM v4.1.0 catalogue and one under an "## AICM ..." section against
# AICM v1.1.0, rather than the AICM-wins union ALL_TITLES. This catches the
# cross-catalogue title confusion the union check is blind to: a handful of
# controls share a code across both matrices but carry a slightly different title
# (e.g. I&S-07 is "Migration to Cloud Environments" in CCM v4.1.0 but "Migration
# to Hosted Environments" in AICM v1.1.0), and because the two titles share content
# words the conservative content-word check below never fires on the mix-up.
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$")

# Known-bad domain codes as BARE standalone tokens (no ``-NN`` suffix, which the
# Check-1 code-validity scan handles). The boundary excludes ``.NET`` (a leading
# dot), the corpus-internal ``AI-GOV`` / ``MODEL-GOV`` identifiers (a leading
# hyphen), and the ``<CODE>-<NN>`` control tokens (a trailing hyphen). Built from
# KNOWN_BAD_DOMAINS so the set stays in sync with the reference module.
_BARE_BAD_ALTERNATION = "|".join(
    re.escape(c) for c in sorted(KNOWN_BAD_DOMAINS, key=len, reverse=True))
BARE_BAD_CODE_RE = re.compile(
    r"(?<![A-Za-z0-9.&\-])(" + _BARE_BAD_ALTERNATION + r")(?![A-Za-z0-9\-])")

# A line names the matrices explicitly (the Check-4 line-local CCM/CSA signal).
# Combined with the section tracker, this scopes the bare-domain-code check so it
# does not fire on ``.NET``, currency ``AUD``, "government" prose, or other
# non-CCM uses of these letters that happen to sit outside any CCM context.
CCM_CONTEXT_RE = re.compile(r"(?i)(CCM|CSA|Cloud Controls Matrix|AICM|AI Controls Matrix)")

# A framework-alignment-table COLUMN HEADER that declares a CSA CCM / AICM column
# (Check 5). Tighter than CCM_CONTEXT_RE (which matches a bare "CSA"): a column
# whose header IS the matrix label, "CSA CCM v4.1", "CSA AICM", "AICM v1.1.0",
# "CCM v4.1", "Cloud Controls Matrix", etc. The check reads codes from that
# column's body cells, so the header must specifically NAME the CCM/AICM matrix,
# not merely mention it mid-phrase: a prose header like "Notes on AICM adoption"
# must NOT be treated as a code column. Anchored at the cell start (cells are
# stripped by split_row), with an optional leading "CSA ", so the matrix label
# must LEAD the header cell; a matrix name buried in prose does not match. Bare
# "CCM v4.1" (no "CSA") is accepted too, closing that false-negative.
CCM_COLUMN_HEADER_RE = re.compile(
    r"(?i)^\s*(?:CSA\s+)?(CCM|Cloud\s+Controls\s+Matrix|AICM|AI\s+Controls\s+Matrix)\b")

# A historical / rename-note / supersession line legitimately names an old code
# while describing its replacement (it is not a current citation), so Check 4
# exempts it. The canonical cases are the glossary I&S rename-note ("Renamed from
# the v4.0 IVS ... domain") and the pack README version-history rows ("corrected
# the superseded CCM v4.0 domain code IVS to ...").
HISTORICAL_RE = re.compile(
    r"(?i)(renamed|superseded|formerly|previously|deprecated|corrected|"
    r"fabricated|no such|does not exist)")

_STOPWORDS = frozenset(
    {"and", "the", "of", "for", "to", "in", "on", "by", "with", "or",
     "a", "an", "&", "is", "as", "at"}
)


def _content_words(title: str) -> set[str]:
    toks = re.split(r"[^A-Za-z0-9]+", title.lower())
    return {t for t in toks if len(t) >= 2 and t not in _STOPWORDS}


def _section_kind(heading_text: str) -> str | None:
    """Classify a heading as a CCM-only, AICM-only, or unscoped section.

    AICM is checked first because an AICM heading may also mention CCM (the AI
    matrix extends the cloud matrix); a heading naming AICM / "AI Controls
    Matrix" is an AICM section even if "CCM" also appears. A heading mentioning
    only CCM / "Cloud Controls Matrix" is a CCM section. Anything else returns
    None, so the title check falls back to the union ALL_TITLES (current
    behaviour) rather than tightening on an ambiguous heading.
    """
    h = heading_text.lower()
    if "aicm" in h or "ai controls matrix" in h:
        return "aicm"
    if "ccm" in h or "cloud controls matrix" in h:
        return "ccm"
    return None


# Controls whose CCM v4.1.0 and AICM v1.1.0 titles diverge by at least one
# distinctive content word. For each such code we record the set of content
# words unique to each catalogue's title; a control-listing row under a CCM
# section that carries an AICM-distinctive word (and none of the CCM-distinctive
# words) is citing the wrong catalogue's title, and vice versa. Controls that
# differ only by punctuation (e.g. IAM-11 "Customers" vs "Customers'") collapse
# to identical content-word sets and so produce no distinctive words: they are
# intentionally NOT policed, consistent with the gate's tolerance of localized
# and abbreviated wording.
def _divergent_controls() -> dict[str, tuple[set[str], set[str]]]:
    out: dict[str, tuple[set[str], set[str]]] = {}
    for code in set(CCM_V41) & set(AICM_V11):
        ccm_t, aicm_t = CCM_V41[code], AICM_V11[code]
        if ccm_t == aicm_t:
            continue
        ccm_w, aicm_w = _content_words(ccm_t), _content_words(aicm_t)
        ccm_only, aicm_only = ccm_w - aicm_w, aicm_w - ccm_w
        if ccm_only and aicm_only:
            out[code] = (ccm_only, aicm_only)
    return out


DIVERGENT_CONTROLS = _divergent_controls()


@dataclass
class Finding:
    path: Path
    line: int
    rule: str
    message: str
    text: str


def split_row(line: str) -> list[str]:
    """Return the stripped cells of a markdown table row (bounding pipes dropped)."""
    parts = line.split("|")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


def is_separator_row(cells: list[str]) -> bool:
    """True for a ``|---|---|`` style separator row."""
    return bool(cells) and set("".join(cells)) <= set("-: ")


def scan_file(path: Path) -> list[Finding]:
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    in_fence = False
    section: str | None = None
    prev_cells: list[str] | None = None  # previous table row, for header lookahead (Check 5)
    ccm_col: int | None = None  # set when the current table has a CSA-CCM/AICM column
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if is_fence_line(line):
            in_fence = not in_fence
            prev_cells = None
            ccm_col = None
            continue
        if in_fence:
            continue

        # Track the current catalogue section for the title check below. A heading
        # also ends any open table, so reset the Check-5 column state.
        hm = HEADING_RE.match(line)
        if hm:
            section = _section_kind(hm.group(1))
            prev_cells = None
            ccm_col = None

        # Check 5: framework-as-column CSA CCM / AICM family-validity. When a
        # framework-alignment table has a column headed "CSA CCM v4.1" (or AICM),
        # every control-code-shaped token in that column must use a real CCM/AICM
        # domain prefix. A token whose prefix is NOT a CCM/AICM domain (valid or
        # known-bad) is invisible to Check 1 (which only policies recognized-family
        # prefixes), so an invented family like ``END-04`` or ``ISM-01`` cited in a
        # CCM column passes silently. This check closes that blind spot (the
        # deep-assessment r1 R11 discovery, PR #782): it reports such a token as
        # an unknown CCM/AICM family. Scoped to the named column only, so a NIST
        # ``AC-2`` in a NIST column or an ISO clause elsewhere is untouched. Known-bad
        # domains (in CCM_FAMILY) stay with Check 1, so there is no double-flag.
        if stripped.startswith("|"):
            cells = split_row(line)
            if is_separator_row(cells):
                if prev_cells is not None and ccm_col is None:
                    for idx, c in enumerate(prev_cells):
                        if CCM_COLUMN_HEADER_RE.search(c):
                            ccm_col = idx
                            break
            else:
                if (ccm_col is not None and len(cells) > ccm_col
                        and not CCM_COLUMN_HEADER_RE.search(cells[ccm_col])):
                    seen_unknown: set[str] = set()
                    for m in CODE_RE.finditer(cells[ccm_col]):
                        domain = m.group(1)
                        if domain in CCM_FAMILY or m.group(0) in seen_unknown:
                            continue
                        seen_unknown.add(m.group(0))
                        findings.append(Finding(
                            path, i, "ccm-unknown-family-in-column",
                            f"'{m.group(0)}' sits in a CSA CCM / AICM column but "
                            f"'{domain}' is not a CCM v4.1 / AICM v1.1 domain "
                            f"(no such domain in the matrices)",
                            line.strip()[:140]))
                prev_cells = cells
        else:
            prev_cells = None
            ccm_col = None

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

        # Check 2: title match on control-listing rows. The lookup is
        # section-aware: under a CCM section the canonical title is the CCM
        # v4.1.0 value, under an AICM section the AICM v1.1.0 value, otherwise
        # the AICM-wins union (preserving the prior behaviour on unscoped tables).
        rm = ROW_RE.match(line)
        if rm:
            code, title = rm.group(1), rm.group(2).strip()
            if section == "ccm":
                canonical = CCM_V41.get(code, ALL_TITLES.get(code))
            elif section == "aicm":
                canonical = AICM_V11.get(code, ALL_TITLES.get(code))
            else:
                canonical = ALL_TITLES.get(code)
            if canonical and title and title.lower() != "control title":
                title_words = _content_words(title)
                if not (title_words & _content_words(canonical)):
                    findings.append(Finding(
                        path, i, "ccm-title-mismatch",
                        f"'{code}' titled '{title}' shares no content word "
                        f"with the catalogue title '{canonical}'",
                        line.strip()[:140]))
                # Check 3 (section-aware): a divergent-title control under a
                # CCM/AICM section whose title carries the OTHER catalogue's
                # distinctive word (and none of this catalogue's) is citing the
                # wrong-version title. The conservative check above cannot see
                # this because the two catalogue titles share content words.
                elif section in ("ccm", "aicm") and code in DIVERGENT_CONTROLS:
                    ccm_only, aicm_only = DIVERGENT_CONTROLS[code]
                    this_only, other_only, other_cat = (
                        (ccm_only, aicm_only, "AICM v1.1.0")
                        if section == "ccm"
                        else (aicm_only, ccm_only, "CCM v4.1.0"))
                    if (title_words & other_only) and not (title_words & this_only):
                        section_label = "CSA CCM v4.1.0" if section == "ccm" else "AICM v1.1.0"
                        findings.append(Finding(
                            path, i, "ccm-title-cross-catalogue",
                            f"'{code}' under a {section_label} section is titled "
                            f"'{title}', which matches the {other_cat} variant, "
                            f"not the {section_label} title '{canonical}'",
                            line.strip()[:140]))

        # Check 4: bare known-bad domain codes (no -NN suffix) in a CCM/CSA
        # context. Catches superseded / fabricated domain *names* (framework
        # family lists, domain-keyed crosswalk rows, glossary-style entries)
        # that carry no <CODE>-<NN> token for Check 1 to see. Scoped to lines
        # that name the matrices OR sit under a CCM/AICM section, and exempting
        # historical rename-notes, so it does not fire on `.NET`, currency
        # `AUD`, "government" prose, or the corpus-internal MODEL-GOV / AI-GOV
        # identifiers. Recall is deliberately bounded to high-confidence CCM
        # contexts (precision-first): a bad code in a multi-framework mapping
        # table where the CCM column is unlabelled on the row and the section
        # heading is generic is NOT caught here; the orchestrator's apply-time
        # standalone-token grep and the periodic /validate sweep cover that tail.
        if not HISTORICAL_RE.search(line) and (
                section in ("ccm", "aicm") or CCM_CONTEXT_RE.search(line)):
            seen_bad: set[str] = set()
            for bm in BARE_BAD_CODE_RE.finditer(line):
                bad = bm.group(1)
                if bad in seen_bad:
                    continue
                seen_bad.add(bad)
                findings.append(Finding(
                    path, i, "ccm-bare-domain-code",
                    f"bare '{bad}' in a CCM/CSA context is not a CCM v4.1 / "
                    f"AICM v1.1 domain code; use {KNOWN_BAD_DOMAINS[bad]}",
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
