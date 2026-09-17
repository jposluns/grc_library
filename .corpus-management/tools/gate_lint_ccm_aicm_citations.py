#!/usr/bin/env python3
"""CSA CCM v4.1.0 / AICM v1.1.0 per-document citation validity - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(Finding, the ref-independent token/heading/context regexes, the helpers
_content_words / _bare_domain_title_mismatch / _section_kind / _divergent_controls,
and scan_file) is the source of record here in the pack. The grc wrapper
(tools/lint-ccm-aicm-citations.py) supplies the CCM/AICM reference catalogue via
configure(ref) and keeps the grc scan scope (collect_targets, EXEMPT_FILES), the
reporting, and the exit codes.

Catalogue-agnostic by construction: the reference catalogue (VALID_DOMAINS,
KNOWN_BAD_DOMAINS, CCM_V41, AICM_V11, ALL_TITLES, DOMAIN_NAMES) and every
structure derived from it (CCM_FAMILY, the bare-domain / bare-bad-code regexes,
DIVERGENT_CONTROLS) are populated by configure(ref), which an adopter calls once
before scanning; the scan logic below is verbatim from the original grc gate and
is unchanged by the split.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

try:
    from aiqt_corpus import is_fence_line, is_separator_row, read_text_safe, split_row
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_ccm_aicm_citations: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Reference catalogue + everything derived from it: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
VALID_DOMAINS: dict = {}
KNOWN_BAD_DOMAINS: dict = {}
CCM_V41: dict = {}
AICM_V11: dict = {}
ALL_TITLES: dict = {}
DOMAIN_NAMES: dict = {}
CCM_FAMILY: frozenset = frozenset()
DIVERGENT_CONTROLS: dict = {}
BARE_BAD_CODE_RE: "re.Pattern | None" = None
BARE_DOMAIN_INLINE_TITLE_RE: "re.Pattern | None" = None
BARE_DOMAIN_COLUMN_TITLE_RE: "re.Pattern | None" = None


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
# the v4.0 IVS ... domain") and the pack README (historically its version-history rows, now retired) ("corrected
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

def _bare_domain_title_mismatch(
        domain: str, title: str, section: str | None) -> bool:
    """Return True when a Check-7 bare-domain title has no safe resolution.

    The overlap denominator is the cited title, matching Check 6's exemption:
    more than half of those content words must occur in the canonical domain or
    a candidate control title. A control-title exemption additionally requires
    one strictly best overlap within the cited domain; a tie is ambiguous and
    therefore is not treated as a resolvable control citation.
    """
    title_words = _content_words(title)
    if not title_words or title_words <= {"domain", "domains"}:
        return False

    domain_words = _content_words(DOMAIN_NAMES.get(domain, ""))
    if domain_words and len(title_words & domain_words) * 2 > len(title_words):
        return False

    if section == "ccm":
        catalogue = CCM_V41
    elif section == "aicm":
        catalogue = AICM_V11
    else:
        catalogue = ALL_TITLES

    best_overlap = 0
    best_codes: list[str] = []
    for code, canonical in catalogue.items():
        if code.rsplit("-", 1)[0] != domain:
            continue
        overlap = len(title_words & _content_words(canonical))
        if overlap * 2 <= len(title_words):
            continue
        if overlap > best_overlap:
            best_overlap = overlap
            best_codes = [code]
        elif overlap == best_overlap:
            best_codes.append(code)
    return len(best_codes) != 1


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


@dataclass
class Finding:
    path: Path
    line: int
    rule: str
    message: str
    text: str


def configure(ref) -> None:
    """Populate the reference catalogue and every structure derived from it.

    ``ref`` supplies the six catalogue symbols (VALID_DOMAINS, KNOWN_BAD_DOMAINS,
    CCM_V41, AICM_V11, ALL_TITLES, DOMAIN_NAMES). The derived structures below are
    verbatim from the original grc gate's module level, only relocated here so the
    engine stays catalogue-agnostic. Call once before scan_file().
    """
    global VALID_DOMAINS, KNOWN_BAD_DOMAINS, CCM_V41, AICM_V11, ALL_TITLES, DOMAIN_NAMES
    global CCM_FAMILY, DIVERGENT_CONTROLS
    global BARE_BAD_CODE_RE, BARE_DOMAIN_INLINE_TITLE_RE, BARE_DOMAIN_COLUMN_TITLE_RE
    VALID_DOMAINS = ref.VALID_DOMAINS
    KNOWN_BAD_DOMAINS = ref.KNOWN_BAD_DOMAINS
    CCM_V41 = ref.CCM_V41
    AICM_V11 = ref.AICM_V11
    ALL_TITLES = ref.ALL_TITLES
    DOMAIN_NAMES = ref.DOMAIN_NAMES

    # CCM/AICM-family domain prefixes worth policing: the valid domains plus the
    # historically-seen wrong ones. A token whose prefix is outside this set (an
    # ISO clause, a NIST 800-53 control like ``AC-2``, a CSF code) is ignored, so
    # the gate does not false-positive on other frameworks' identifiers.
    CCM_FAMILY = frozenset(VALID_DOMAINS) | frozenset(KNOWN_BAD_DOMAINS)

    # Known-bad domain codes as BARE standalone tokens (no ``-NN`` suffix, which the
    # Check-1 code-validity scan handles). The boundary excludes ``.NET`` (a leading
    # dot), the corpus-internal ``AI-GOV`` / ``MODEL-GOV`` identifiers (a leading
    # hyphen), and the ``<CODE>-<NN>`` control tokens (a trailing hyphen). Built from
    # KNOWN_BAD_DOMAINS so the set stays in sync with the reference module.
    _BARE_BAD_ALTERNATION = "|".join(
        re.escape(c) for c in sorted(KNOWN_BAD_DOMAINS, key=len, reverse=True))
    BARE_BAD_CODE_RE = re.compile(
        r"(?<![A-Za-z0-9.&\-])(" + _BARE_BAD_ALTERNATION + r")(?![A-Za-z0-9\-])")

    # A valid CCM/AICM DOMAIN as a bare token, not a numbered control. Check 7 uses
    # the first expression for the explicit code-first inline-title forms and the
    # second for a domain+title value in a table column already identified by
    # CCM_COLUMN_HEADER_RE. The latter is anchored at the cell start so a later
    # acronym in prose cannot be mistaken for the cited domain. ``AIS, TVM Domains``
    # does not match: the comma after AIS is not a title introducer and TVM is not at
    # the cell start.
    _BARE_DOMAIN_ALTERNATION = "|".join(
        re.escape(c) for c in sorted(VALID_DOMAINS, key=len, reverse=True))
    BARE_DOMAIN_INLINE_TITLE_RE = re.compile(
        r"(?<![A-Za-z0-9.&\-])(" + _BARE_DOMAIN_ALTERNATION
        + r")(?![A-Za-z0-9\-])(?:\s*:\s*([^|.;]+)|\s*\(([^|()]+)\))")
    BARE_DOMAIN_COLUMN_TITLE_RE = re.compile(
        r"^\s*(" + _BARE_DOMAIN_ALTERNATION
        + r")(?![A-Za-z0-9\-])(?:\s*:\s*|\s+)(.+?)\s*$")

    DIVERGENT_CONTROLS = _divergent_controls()


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

                # Check 6: wrong control TITLE in a framework-LABEL row. In a table
                # where each row names its framework in a cell (e.g.
                # "| CSA CCM v4.1 | IAM-15: <title> |"), the code+title sit in the
                # cell AFTER the framework-label cell, so Check 2's ROW_RE (code in
                # the FIRST cell) never sees them. This catches the Sweep-129 GRC-01
                # class: a code whose cited title shares NO content word with the
                # catalogue control title (GRC-01 "Governance Program" cited as
                # "Risk Management Framework"). EXEMPTION (domain-name-as-title,
                # maintainer-decided 2026-08-01): a title that renders the code's
                # DOMAIN name rather than the control title is a legitimate
                # cite-the-domain convention, exempt when MORE THAN HALF the title's
                # content words appear in the code's domain name (DOMAIN_NAMES,
                # source-verified vs the CCM/AICM catalogues). FP-safe in practice:
                # GRC-01 "Risk Management Framework" has only "risk" of 3 words in the
                # GRC domain "Governance, Risk and Compliance" (1/3, not > 1/2) so it
                # still flags, while IAM-15 "Identity and Access Management" has 3/3 in
                # the IAM domain and is exempt. Family/range validity is Check 1/5's
                # job, so this check skips a non-family or known-bad prefix.
                for ci, cell in enumerate(cells):
                    if not CCM_COLUMN_HEADER_RE.search(cell) or ci + 1 >= len(cells):
                        continue
                    code_ms = list(CODE_RE.finditer(cells[ci + 1]))
                    if len(code_ms) != 1:
                        continue
                    cm = code_ms[0]
                    code6, dom6 = cm.group(0), cm.group(1)
                    if dom6 not in CCM_FAMILY or dom6 in KNOWN_BAD_DOMAINS:
                        continue
                    title6 = cells[ci + 1][cm.end():].lstrip(": ").strip()
                    if not title6:
                        continue
                    if section == "ccm":
                        canon6 = CCM_V41.get(code6, ALL_TITLES.get(code6))
                    elif section == "aicm":
                        canon6 = AICM_V11.get(code6, ALL_TITLES.get(code6))
                    else:
                        canon6 = ALL_TITLES.get(code6)
                    if not canon6:
                        continue
                    tw6 = _content_words(title6)
                    if not tw6 or (tw6 & _content_words(canon6)):
                        continue  # shares a control-title word -> not a mismatch
                    # Domain-name exemption uses the BASE title (the part before a trailing
                    # ": <qualifier>", e.g. "Encryption and Key Management" from
                    # "Encryption and Key Management: PKI"), so a verbose context qualifier
                    # cannot dilute the domain-name overlap below the threshold and cry wolf on
                    # a legitimate cite-the-domain reference (codex vpr3186 E2: the expanded
                    # "...: Public Key Infrastructure (PKI)" form would otherwise fall to 3/6).
                    base6 = _content_words(title6.split(":", 1)[0])
                    dw6 = _content_words(DOMAIN_NAMES.get(dom6, ""))
                    if dw6 and base6 and len(base6 & dw6) * 2 > len(base6):
                        continue  # > half the BASE title's words are the domain name -> exempt
                    findings.append(Finding(
                        path, i, "ccm-title-mismatch-in-column",
                        f"'{code6}' titled '{title6}' shares no content word with "
                        f"the catalogue title '{canon6}' (nor the '{dom6}' domain name)",
                        line.strip()[:140]))
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

        # Check 7: wrong inline TITLE after a valid BARE domain code. Numbered
        # control-title checks cannot see ``SEF: Software Engineering and
        # Development`` because there is no ``SEF-NN`` token. Inspect only
        # code-first colon/parenthetical forms in explicit CCM/AICM context, or
        # the leading domain+title value in a table column whose header declares
        # CSA CCM / AICM. A domain name and a uniquely best matching control
        # title are both legitimate expansions; the shared helper applies the
        # same strict greater-than-half content-word threshold as Check 6.
        domain_titles: list[tuple[str, str]] = []
        if section in ("ccm", "aicm") or CCM_CONTEXT_RE.search(line):
            for dm in BARE_DOMAIN_INLINE_TITLE_RE.finditer(line):
                domain_titles.append((dm.group(1), dm.group(2) or dm.group(3)))
        if stripped.startswith("|") and ccm_col is not None:
            check7_cells = split_row(line)
            if len(check7_cells) > ccm_col:
                dm = BARE_DOMAIN_COLUMN_TITLE_RE.match(check7_cells[ccm_col])
                if dm and not CODE_RE.search(check7_cells[ccm_col]):
                    domain_titles.append((dm.group(1), dm.group(2)))

        seen_domain_titles: set[tuple[str, str]] = set()
        for domain7, title7 in domain_titles:
            title7 = title7.strip().strip("()")
            key7 = (domain7, title7)
            if key7 in seen_domain_titles:
                continue
            seen_domain_titles.add(key7)
            if _bare_domain_title_mismatch(domain7, title7, section):
                findings.append(Finding(
                    path, i, "ccm-bare-domain-title-mismatch",
                    f"bare domain '{domain7}' titled '{title7}' matches neither "
                    f"the domain name '{DOMAIN_NAMES[domain7]}' nor a uniquely "
                    f"resolvable {domain7} control title",
                    line.strip()[:140]))
    return findings
