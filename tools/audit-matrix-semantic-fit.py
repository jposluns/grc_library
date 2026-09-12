#!/usr/bin/env python3
"""Advisory semantic-fit pre-filter for the compliance matrix and source-doc
framework tables (the gate-blind "valid code, wrong control" class).

WHAT THIS IS (and is NOT). This is a maintainer dev-AID, not an audit gate. The
audit gates 48/49/54/58/61 check that a cited control code EXISTS in its framework
catalogue (and, for gate 49, that it is in the right catalogue). None of them
check semantic FIT: whether the control a row cites is the right control for
that row's document. That class ("valid code, wrong control") is gate-blind and
has recurred (the 2026-06-27 trust-recovery `/full-qa` found 8 matrix + 7
source-doc instances; improvement-log #392). Semantic fit is not mechanically
gate-checkable, so the durable instrument is a cadenced human/subagent audit
(the `/matrix-fit` skill). This aid is the cheap, RECALL-ORIENTED TRIAGE step
that feeds that audit: it narrows the audit's scope to the rows that lack any
lexical anchor between the document subject and its cited control titles, so the
semantic judge (the skill, and the human reading its output) can focus there
first. It does NOT judge fit, and it does NOT claim a listed row is wrong; it
hands the semantic audit a worklist. Non-listed rows (those with a lexical
anchor) are DEPRIORITIZED, not certified correct.

It is NOT precision-first, and the docstring section below records why: a stdlib
lexical signal is too weak to be precision-first for this class (its strictest
setting still lists ~64 rows on the clean post-#392 corpus, because correct GRC
mappings routinely share no vocabulary with the document title, e.g. "Document
Index and Classification" -> GRC-01 "Governance Program Policy and Procedures").
So the tool is the audit's input-narrowing step, not a standalone reporter.

It is named ``audit-*`` (not ``lint-*``) so the gate machinery (the four-surface
parity gate 35, the regression suite gate 36) does NOT auto-discover it, and it
is NOT wired into ``run_all_audits.sh`` / ``quality.yml`` / ``.pre-commit-config.yaml``.
It always exits 0 (it reports candidates; it never fails a workflow), because a
lexical pre-filter is intentionally low-recall and its "flags" are candidates,
not defects. Making it a blocking gate would be a decorative gate (gate-discipline
rule): it would either be too noisy to trust or too strict to add value, and the
real check is the semantic audit it feeds. Its self-test lives behind
``--self-test`` (inline unittest) rather than in ``tests/`` so the gate-36
regression runner does not adopt it as a gated test.

RECALL-ORIENTED TRIAGE by design (maintainer decision, 2026-06-27, taken after
the lexical signal empirically listed ~64 rows on the clean corpus and so could
not serve as a precision-first reporter). A row lands on the worklist when,
across every cited control whose title this aid knows (CCM v4.1 via ``CCM_V41``;
CSA AICM v1.1 via ``AICM_V11``, which supplies titles for the AI-specific
AICM-only delta carried in the matrix's "CSA AICM v1.1" column; NIST CSF 2.0
categories via ``CSF_CATEGORIES``; COBIT 2019 objectives via ``COBIT_OBJECTIVES``; and ISO/IEC 27001:2022 Annex A controls via ``ISO27001_2022_ANNEX_A``), NO control's title shares a
single significant word with the document subject. A single anchoring code (a
sibling whose title overlaps the subject) keeps the row OFF the worklist, both
because matrix rows legitimately carry a primary mapping plus looser supporting
codes and because the goal is to narrow the semantic audit's scope, not to
adjudicate. The subtler "loose supporting code on an otherwise-anchored row"
case (e.g. matrix row 163's TVM-06 on a pen-testing standard, Sweep-61 note
A-note-1) is intentionally NOT on the worklist: an anchored row is deprioritized,
and that residual case is exactly what the semantic `/matrix-fit` skill catches.
ISO/IEC 27001:2022 Annex A controls ARE assessed (via the 93-control
iso27001_reference title map, the 2026-09-02 extension closing the pre-filter's
ISO blind spot); COBIT 2019 objective titles are assessable via the
cobit_iso31000_reference extension. ISO 31000 clause headings are deliberately
NOT code-matched: a bare clause token carries no framework identity, so no
CODE_RE branch reads them and they are left to the manual /matrix-fit audit. Rows with
no known-title code (or whose subject carries no significant token) are counted
UNASSESSABLE and LISTED as an advisory feeder for the /matrix-fit judge (the title is
read from the reference-base extract, or the judge records `title-not-held` when it is
absent there too); they are never silently folded into the assessed count (P-1.83 M5
honest counts). Framework columns with no wired title map (the sector columns) are
surfaced as an unassessed-columns advisory rather than silently skipped (P-1.83 M3).

WHAT IT SCANS:
  * The compliance matrix (``compliance/matrix-grc-compliance-alignment.md``):
    each per-domain mapping table row, subject = the "Document Title" cell with
    its "Type:" prefix dropped.
  * Source-doc framework tables: each corpus document's ``## ... Framework
    alignment`` section (table ``| Framework | Reference | Topic |``); subject =
    the document's H1 title.

Exit code: always 0. Usage:
    python3 tools/audit-matrix-semantic-fit.py                 # scan both surfaces
    python3 tools/audit-matrix-semantic-fit.py --matrix-only
    python3 tools/audit-matrix-semantic-fit.py --source-docs-only
    python3 tools/audit-matrix-semantic-fit.py --self-test     # run inline unit tests
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from ccm_aicm_reference import AICM_V11, CCM_V41
from cobit_iso31000_reference import COBIT_OBJECTIVES
from nist_csf_reference import CSF_CATEGORIES
from iso27001_reference import ISO27001_2022_ANNEX_A
from matrix_code_parse import CODE_RE  # shared canonical parser (P-1.62 I10)

try:
    from lint_common import AUDITED_DOMAIN_DIRS
except Exception:  # pragma: no cover - lint_common shape is stable; fallback keeps the aid runnable
    AUDITED_DOMAIN_DIRS = (
        "ai", "architecture", "compliance", "crypto", "dev-security", "governance",
        "operations", "privacy", "resilience", "risk", "security", "supply-chain",
    )

REPO_ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = REPO_ROOT / "compliance" / "matrix-grc-compliance-alignment.md"

# Combined code -> title lookup the aid can assess against (CCM v4.1 + AICM v1.1
# + CSF 2.0 categories + COBIT 2019 objectives + ISO/IEC
# 27001:2022 Annex A controls). AICM v1.1 is the AI-focused extension of CCM v4.1;
# as an implementation
# detail its code-set carries the CCM base plus 40 AICM-only codes (identical
# titles for the shared base). Updating AICM_V11 folds in the AICM-only titles so
# the matrix's "CSA AICM v1.1" column (which carries those AICM-only codes) is
# assessable; the shared-base titles are unchanged by the update.
KNOWN_TITLES: dict[str, str] = {}
KNOWN_TITLES.update(CCM_V41)
KNOWN_TITLES.update(AICM_V11)
KNOWN_TITLES.update(CSF_CATEGORIES)
# COBIT 2019 objective titles (the 2026-07-02 extension; gate-blind fit
# judgment for a family gates 48/49/54/58 do not cover, per the PR #587
# build). Practice-level COBIT
# titles are deliberately absent from the reference module (extraction wraps
# them), so practice codes are existence-checked by the companion gate and
# fit-assessed here only at the objective level.
KNOWN_TITLES.update(COBIT_OBJECTIVES)
# ISO/IEC 27001:2022 Annex A control titles (the 93-control closed set, keyed
# "A.<theme>.<n>" as the corpus/matrix cite them). Added because the ISO family
# was the pre-filter's blind spot: the P-1.63 stranded-code incident (A.8.10 ->
# A.7.10, #1914) was a valid-code-wrong-control miss in exactly this family, which
# gate 58 (Annex A existence) cannot see. Now assessable at the control-title level.
KNOWN_TITLES.update(ISO27001_2022_ANNEX_A)

# Control-code token CODE_RE (CCM/AICM + CSF category + COBIT objective/practice +
# ISO/IEC 27001:2022 Annex A) is the shared canonical parser, imported above from
# tools/matrix_code_parse.py (unified with audit-stranded-matrix-code, P-1.62 I10).

# Minimal stopword set: only words with no discriminating power. Kept SMALL on
# purpose - a larger set would strip real overlap and over-flag (the opposite of
# precision-first). Document-type prefixes ("standard", "policy", ...) are
# stripped separately from the matrix subject, not treated as stopwords here.
STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "with",
    "by", "as", "at", "is", "are", "be", "this", "that", "its", "their",
}

# Document-type prefixes that lead a matrix "Document Title" cell; dropped from
# the subject so the subject is the document's actual topic.
TYPE_PREFIXES = {
    "policy", "standard", "procedure", "register", "framework", "guideline",
    "charter", "guide", "playbook", "plan",
}


def significant_tokens(text: str) -> set[str]:
    """Lowercased word tokens, stopwords and very short tokens removed."""
    toks = re.findall(r"[a-z0-9]+", text.lower())
    return {t for t in toks if len(t) >= 3 and t not in STOPWORDS}


def token_match(a: str, b: str) -> bool:
    """Two tokens match if equal, or (for longer tokens) share a >=5-char prefix.

    The prefix rule lets English derivations match (classification/classify,
    authentication/authenticate) without aggressive stemming.
    """
    if a == b:
        return True
    if len(a) >= 5 and len(b) >= 5:
        n = 0
        for ca, cb in zip(a, b):
            if ca != cb:
                break
            n += 1
        return n >= 5
    return False


def overlap_count(subject: set[str], title_tokens: set[str]) -> int:
    """Number of subject tokens that match at least one title token."""
    return sum(1 for s in subject if any(token_match(s, t) for t in title_tokens))


def strip_type_prefix(title_cell: str) -> str:
    """Drop a leading 'Type:' prefix from a matrix Document-Title cell."""
    if ":" in title_cell:
        head, rest = title_cell.split(":", 1)
        if head.strip().lower() in TYPE_PREFIXES:
            return rest.strip()
    return title_cell.strip()


def assess_row(subject_text: str, codes: list[str]) -> dict | None:
    """Return a worklist dict if the row lacks a lexical anchor, else None.

    A row lands on the worklist iff at least one cited code has a known title AND
    no known-title code shares a single significant token with the subject. This
    is a recall-oriented narrowing for the semantic audit, NOT a precision-first
    judgement that the row is wrong. A worklist dict also carries
    ``unknown_codes``: the row's cited codes with NO held title in the validator
    modules, printed as title-not-held candidates for the /matrix-fit judge
    (P-1.83 M6), who reads each from the reference-base extract or records
    `title-not-held` when it is absent there too.
    """
    subject = significant_tokens(subject_text)
    if not subject:
        return None
    known = [(c, KNOWN_TITLES[c]) for c in codes if c in KNOWN_TITLES]
    if not known:
        return None  # no code carries a known title -> nothing to assess, do not flag
    unknown_codes: list[str] = []
    for c in codes:
        if c not in KNOWN_TITLES and c not in unknown_codes:
            unknown_codes.append(c)
    best = 0
    per_code = []
    for code, title in known:
        score = overlap_count(subject, significant_tokens(title))
        per_code.append((code, title, score))
        best = max(best, score)
    if best == 0:
        return {"subject": subject_text, "codes": per_code,
                "unknown_codes": unknown_codes}
    return None


def row_assessable(subject_text: str, codes: list[str]) -> bool:
    """True iff the row is pre-filter-assessable: the subject carries at least
    one significant token AND at least one cited code has a held title in
    KNOWN_TITLES. Every other parsed row is counted unassessable and listed as
    the semantic judge's feeder, never silently folded into the assessed count
    (P-1.83 M5 honest counts)."""
    return bool(significant_tokens(subject_text)) and any(
        c in KNOWN_TITLES for c in codes)


# --- Matrix parsing ---------------------------------------------------------

# Mapping-table header labels: the framework columns this pre-filter ASSESSES (a
# code -> title map is wired for each) and the non-framework label columns. Any
# OTHER header cell in a recognized mapping table is a framework column the
# pre-filter cannot assess (no held title map: the sector columns CTPAT / PIP /
# BASC v6 / WCO SAFE / AEO/AEO-S), accumulated and surfaced as an
# unassessed-columns ADVISORY (P-1.83 M3) so those citations visibly reach the
# /matrix-fit judge instead of silently vanishing from the counts.
ASSESSED_COLUMN_LABELS = {
    "CSA CCM v4.1", "CSA AICM v1.1", "NIST CSF 2.0", "COBIT 2019",
    "ISO/IEC 27001:2022",
}
NON_FRAMEWORK_COLUMN_LABELS = {"Domain", "Document Title", "Path"}

def _split_row(line: str) -> list[str]:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def scan_matrix(path: Path, docs=None) -> tuple[list[dict], dict]:
    """Scan the compliance matrix's per-domain mapping tables.

    Returns (candidates, stats). stats carries the HONEST counts (P-1.83 M5):
    ``n_assessed`` counts ONLY truly-assessable rows (per row_assessable: a
    significant subject AND at least one cited code with a held title);
    ``n_unassessable`` counts parsed rows that are NOT assessable, each listed
    in ``stats["unassessable"]`` as ``{location, subject, codes}`` so the
    /matrix-fit judge has a feeder; ``n_unparsed_tables`` is the count of
    "Document Title"+"Path" header rows whose "CSA CCM v4.1" column was renamed
    (a table silently skipped, a PARTIAL parse failure);
    ``unassessed_columns`` (P-1.83 M3) lists framework columns present in a
    recognized header but carrying no wired title map. n_assessed == 0 AND
    n_unassessable == 0 means the header anchor was never matched (a
    reworded/renamed column), i.e. a PARSE FAILURE, NOT a clean surface: the
    caller must refuse to assert cleanliness in that case (guard-inputs
    discipline; make ignorance a first-class return that refuses rather than
    permits).
    """
    candidates: list[dict] = []
    n_assessed = 0
    n_unassessable = 0
    unassessable: list[dict] = []
    unassessed_columns: set[str] = set()
    n_unparsed_tables = 0  # candidate mapping-table headers ("Document Title" + "Path") whose
    # "CSA CCM v4.1" column was renamed (a table silently skipped): counted DIRECTLY as
    # |candidate \ recognized| in the loop below, so it is exact and never negative (P-1.85).
    # A subtraction of the two aggregate counts was WRONG: a Path-less recognized table
    # (recognized, not candidate) could cancel a genuine renamed-CCM table and mask it.
    lines = path.read_text(encoding="utf-8").splitlines()
    title_idx = ccm_idx = aicm_idx = csf_idx = cobit_idx = iso_idx = path_idx = None
    in_table = False
    for raw, line in enumerate(lines, start=1):
        if line.lstrip().startswith("|"):
            cells = _split_row(line)
            # A candidate mapping-table header carries BOTH stable label columns
            # ("Document Title" and "Path"); requiring both stops a lone data cell whose
            # value is literally "Document Title" from masquerading as a header. A candidate
            # whose "CSA CCM v4.1" column was renamed (absent) is an UNPARSED table: counted
            # directly here so the count is exact per-table, never a cancelling subtraction.
            if ("Document Title" in cells and "Path" in cells
                    and "CSA CCM v4.1" not in cells):
                n_unparsed_tables += 1
            # Header row of a mapping table?
            if "Document Title" in cells and "CSA CCM v4.1" in cells:
                title_idx = cells.index("Document Title")
                ccm_idx = cells.index("CSA CCM v4.1")
                aicm_idx = cells.index("CSA AICM v1.1") if "CSA AICM v1.1" in cells else None
                csf_idx = cells.index("NIST CSF 2.0") if "NIST CSF 2.0" in cells else None
                cobit_idx = cells.index("COBIT 2019") if "COBIT 2019" in cells else None
                iso_idx = (cells.index("ISO/IEC 27001:2022")
                           if "ISO/IEC 27001:2022" in cells else None)
                path_idx = cells.index("Path") if "Path" in cells else None
                unassessed_columns.update(
                    c for c in cells
                    if c and c not in ASSESSED_COLUMN_LABELS
                    and c not in NON_FRAMEWORK_COLUMN_LABELS)
                in_table = True
                continue
            if not in_table or title_idx is None:
                continue
            if set(cells) <= {"", "---"} or all(set(c) <= {"-"} for c in cells if c):
                continue  # separator row
            if len(cells) <= ccm_idx:
                continue
            if docs is not None:  # per-batch scope: keep only rows referencing a scoped doc
                rowdoc = None
                if path_idx is not None and len(cells) > path_idx:
                    m = (re.search(r"`([^`]+\.md)`", cells[path_idx])
                         or re.search(r"\]\((?:\.\./)?([^)]+\.md)\)", cells[path_idx]))
                    rowdoc = m.group(1) if m else None
                if rowdoc is None or rowdoc not in docs:
                    continue
            subject = strip_type_prefix(cells[title_idx])
            codes = CODE_RE.findall(cells[ccm_idx])
            if aicm_idx is not None and len(cells) > aicm_idx:
                codes += CODE_RE.findall(cells[aicm_idx])
            if csf_idx is not None and len(cells) > csf_idx:
                codes += CODE_RE.findall(cells[csf_idx])
            if cobit_idx is not None and len(cells) > cobit_idx:
                codes += CODE_RE.findall(cells[cobit_idx])
            if iso_idx is not None and len(cells) > iso_idx:
                codes += CODE_RE.findall(cells[iso_idx])
            try:
                rel = path.relative_to(REPO_ROOT)
            except ValueError:  # a path outside the repo (e.g. a self-test temp file)
                rel = path
            location = f"{rel}:{raw}"
            if row_assessable(subject, codes):
                n_assessed += 1
                result = assess_row(subject, codes)
                if result:
                    result["location"] = location
                    candidates.append(result)
            else:
                n_unassessable += 1
                unassessable.append(
                    {"location": location, "subject": subject, "codes": codes})
        else:
            in_table = False
            title_idx = ccm_idx = aicm_idx = csf_idx = cobit_idx = iso_idx = path_idx = None
    # A "Document Title" header row whose "CSA CCM v4.1" column was renamed is a table
    # the scan silently skipped (a PARTIAL parse failure). Residue: a table whose
    # "Document Title" column itself was renamed is invisible to this candidate count.
    stats = {
        "n_assessed": n_assessed,
        "n_unassessable": n_unassessable,
        "n_unparsed_tables": n_unparsed_tables,
        "unassessable": unassessable,
        "unassessed_columns": sorted(unassessed_columns),
    }
    return candidates, stats


# --- Source-doc framework-table parsing -------------------------------------

FRAMEWORK_HEADING_RE = re.compile(r"^#{2,3}\s.*framework alignment", re.IGNORECASE)
H1_RE = re.compile(r"^#\s+(.*\S)\s*$")


def _doc_title(lines: list[str]) -> str | None:
    for line in lines:
        m = H1_RE.match(line)
        if m:
            return m.group(1).strip()
    return None


def scan_source_doc(path: Path) -> tuple[str, list[str], bool, int]:
    """Extract one document's framework-alignment (subject, codes, had_table, section_line).

    subject is the document's H1 title ("" when the document has no H1, which
    row_assessable then counts as unassessable rather than skipping a parsed
    table); had_table is True when the framework-alignment section yielded at
    least one parseable control code; section_line is the 1-based line of the
    framework-alignment SECTION HEADING (0 if none found), so the worklist can
    cite ``path:line`` uniformly with the matrix surface (P-1.83 N4). The
    assessable/unassessable classification lives in scan_source_docs (P-1.83 M5)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    subject = _doc_title(lines) or ""
    # Locate the framework-alignment section and collect codes from its table.
    in_section = False
    section_line = 0
    codes: list[str] = []
    for lineno, line in enumerate(lines, start=1):
        if line.startswith("#"):
            in_section = bool(FRAMEWORK_HEADING_RE.match(line))
            if in_section and section_line == 0:
                section_line = lineno  # first framework-alignment heading
            continue
        if in_section and line.lstrip().startswith("|"):
            codes += CODE_RE.findall(line)
    return subject, codes, bool(codes), section_line


def scan_source_docs(docs=None) -> tuple[list[dict], dict]:
    """Scan every corpus document's framework-alignment table. Recurses into domain
    SUBDIRECTORIES (sector annexes under compliance/<sector>/, jurisdiction annexes
    under ai/jurisdictions/, ...) via rglob, matching the docstring's "each corpus
    document" claim. Returns (candidates, stats) in scan_matrix's stats shape
    (P-1.83 M5): n_assessed counts docs whose framework table is truly assessable
    (per row_assessable); n_unassessable counts docs whose parsed table is NOT,
    each listed in stats["unassessable"]; n_unparsed_tables is always 0 here
    (source docs are per-doc, no multi-table partial case) and unassessed_columns
    is always [] (framework identity is per-ROW in these tables, not a header
    column). Both counts 0 means no framework table was parsed at all: a PARSE
    FAILURE, not a clean result."""
    candidates: list[dict] = []
    n_assessed = 0
    n_unassessable = 0
    unassessable: list[dict] = []
    for domain in AUDITED_DOMAIN_DIRS:
        d = REPO_ROOT / domain
        if not d.is_dir():
            continue
        for md in sorted(d.rglob("*.md")):
            if md.resolve() == MATRIX_PATH.resolve():
                continue
            if docs is not None and md.relative_to(REPO_ROOT).as_posix() not in docs:
                continue
            subject, codes, had_table, section_line = scan_source_doc(md)
            if not had_table:
                continue
            try:
                location = f"{md.relative_to(REPO_ROOT)}:{section_line}"
            except ValueError:  # a path outside the repo (e.g. a self-test temp file)
                location = f"{md}:{section_line}"
            if row_assessable(subject, codes):
                n_assessed += 1
                result = assess_row(subject, codes)
                if result:
                    result["location"] = location
                    candidates.append(result)
            else:
                n_unassessable += 1
                unassessable.append(
                    {"location": location, "subject": subject, "codes": codes})
    stats = {
        "n_assessed": n_assessed,
        "n_unassessable": n_unassessable,
        "n_unparsed_tables": 0,  # source docs are per-doc: no multi-table partial case
        "unassessable": unassessable,
        "unassessed_columns": [],  # framework identity is per-row here, not a column
    }
    return candidates, stats


# --- Reporting --------------------------------------------------------------

def report(candidates: list[dict], stats: dict, surface: str) -> None:
    n_assessed = stats["n_assessed"]
    n_unassessable = stats["n_unassessable"]
    n_unparsed = stats["n_unparsed_tables"]
    unassessable = stats.get("unassessable", [])
    unassessed_columns = stats.get("unassessed_columns", [])
    if n_assessed == 0 and n_unassessable == 0:
        print(f"  {surface}: PARSE-FAILURE - 0 rows assessed. The header/table anchor was "
              f"NOT found (a renamed or reworded column), so the scan could not read this "
              f"surface. This is NOT a clean result; do not trust the worklist as empty.")
        return
    if n_unparsed > 0:
        print(f"  {surface}: PARTIAL-PARSE WARNING - {n_unparsed} mapping table(s) had a "
              f"'Document Title' header but no recognized 'CSA CCM v4.1' column (a renamed "
              f"column), so those tables were SKIPPED. The worklist below is INCOMPLETE.")
    if unassessed_columns:
        print(f"  {surface}: ADVISORY - {len(unassessed_columns)} header column(s) in the "
              f"mapping tables carry no held title map, so this pre-filter does not "
              f"assess their codes: {', '.join(unassessed_columns)}. The /matrix-fit judge "
              f"covers them from the reference-base extracts (`title-not-held` if absent "
              f"there too).")
    if n_unassessable > 0:
        print(f"  {surface}: {n_unassessable} row(s) not pre-filter-assessable (no cited code "
              f"carries a held title in the validator modules, or the subject has no "
              f"significant tokens); judge from the reference-base extracts "
              f"(`title-not-held` if absent there too):")
        for u in unassessable:
            print(f"    - {u['location']}  subject: {u['subject']!r}  codes: {u['codes']}")
    if not candidates:
        if n_assessed == 0:
            print(f"  {surface}: 0 row(s) assessed; ALL {n_unassessable} parsed row(s) are "
                  f"unassessable (listed above). NOT a clean result: this pre-filter could "
                  f"not judge the surface; the /matrix-fit skill must.")
        elif n_unassessable == 0:
            print(f"  {surface}: assessed {n_assessed} row(s), 0 on the worklist "
                  f"(every assessed row has a lexical anchor).")
        else:
            print(f"  {surface}: assessed {n_assessed} row(s), 0 on the worklist "
                  f"(every assessed row has a lexical anchor; {n_unassessable} row(s) not "
                  f"assessable, listed above).")
        return
    print(f"  {surface}: assessed {n_assessed} row(s), {len(candidates)} on the semantic-audit worklist:")
    for c in candidates:
        print(f"    - {c['location']}  subject: {c['subject']!r}")
        for code, title, score in c["codes"]:
            print(f"        {code} = {title!r} (overlap {score})")
        if c.get("unknown_codes"):
            print(f"        title-not-held candidates for the judge (no held title): "
                  f"{', '.join(c['unknown_codes'])}")


def run(matrix: bool, source_docs: bool, docs=None, as_json=False) -> int:
    docset = None if docs is None else {str(Path(d).as_posix()) for d in docs}
    if as_json:
        import json as _json
        out = {"scoped_docs": (sorted(docset) if docset is not None else None)}
        def _wl(cands):
            return [{"location": c["location"], "subject": c["subject"],
                     "codes": [{"code": code, "title": title, "overlap": score}
                               for code, title, score in c["codes"]],
                     "unknown_codes": c.get("unknown_codes", [])} for c in cands]
        if matrix:
            cands, stats = scan_matrix(MATRIX_PATH, docset)
            out["matrix"] = {"assessed": stats["n_assessed"],
                             "n_unassessable": stats["n_unassessable"],
                             "n_unparsed_tables": stats["n_unparsed_tables"],
                             "unassessable": stats["unassessable"],
                             "unassessed_columns": stats["unassessed_columns"],
                             "worklist": _wl(cands)}
        if source_docs:
            cands, stats = scan_source_docs(docset)
            out["source_docs"] = {"assessed": stats["n_assessed"],
                                  "n_unassessable": stats["n_unassessable"],
                                  "unassessable": stats["unassessable"],
                                  "unassessed_columns": stats["unassessed_columns"],
                                  "worklist": _wl(cands)}
        print(_json.dumps(out, indent=2))
        return 0
    print("ADVISORY semantic-fit TRIAGE worklist for the /matrix-fit audit (NOT a gate; exit 0 always).")
    print("Listed rows lack a lexical anchor; they are the audit's worklist, NOT confirmed defects.")
    print("Non-listed rows are deprioritized, NOT certified; the /matrix-fit skill adjudicates fit.\n")
    if matrix:
        cands, stats = scan_matrix(MATRIX_PATH, docset)
        report(cands, stats, "Compliance matrix")
    if source_docs:
        cands, stats = scan_source_docs(docset)
        report(cands, stats, "Source-doc framework tables")
    print(
        "\nThe /matrix-fit semantic audit judges each listed row against the source control "
        "TITLE (CCM v4.1 / AICM v1.1 / CSF 2.0 / COBIT 2019 / "
        "ISO/IEC 27001:2022). A "
        "worklisted row is a focus candidate, not a "
        "mismatch; a non-worklisted row may still carry a loose supporting code (the skill covers those too)."
    )
    return 0


# --- Inline self-test (kept out of tests/ so gate 36 does not adopt it) ------

def _self_test() -> int:
    import unittest

    def _stats(n_assessed=0, n_unassessable=0, n_unparsed_tables=0,
               unassessable=None, unassessed_columns=None):
        """Build a full scanner-shape stats dict for report() tests."""
        return {"n_assessed": n_assessed, "n_unassessable": n_unassessable,
                "n_unparsed_tables": n_unparsed_tables,
                "unassessable": unassessable or [],
                "unassessed_columns": unassessed_columns or []}

    class SemanticFitTests(unittest.TestCase):
        def test_clear_mismatch_flagged(self):
            # Pre-#392 row 52 shape: "Records Retention and Destruction" cited
            # DSP-07/DSP-08 (by-design privacy), no token overlap -> flagged.
            r = assess_row(
                "Records Retention and Destruction",
                ["DSP-07", "DSP-08"],
            )
            self.assertIsNotNone(r)

        def test_good_match_not_flagged(self):
            # Post-#392 row 52: DSP-16 "Data Retention and Deletion" overlaps
            # "Retention" -> rescued, not flagged.
            r = assess_row(
                "Records Retention and Destruction",
                ["DSP-16", "DSP-02"],
            )
            self.assertIsNone(r)

        def test_sibling_rescue_keeps_row_off_worklist(self):
            # An anchored row stays off the worklist even if it carries a loose
            # supporting code: "Penetration Testing and Red Team" with the
            # bullseye TVM-07 present is deprioritized (the /matrix-fit skill,
            # not this triage step, catches the residual loose-TVM-06 case).
            r = assess_row(
                "Penetration Testing and Red Team",
                ["TVM-07", "TVM-06"],  # TVM-07 = "Penetration Testing" rescues
            )
            self.assertIsNone(r)

        def test_iso27001_only_row_assessed(self):
            # ISO/IEC 27001:2022 Annex A codes now carry titles (the 2026-09-02
            # iso27001_reference extension), so an ISO-only row participates.
            # A.5.33 = "Protection of records", A.8.10 = "Information deletion":
            # neither shares a token with "Some Document" -> the row lands on the
            # worklist (recall-oriented), where before it was skipped as unassessable.
            self.assertEqual(KNOWN_TITLES["A.5.33"], "Protection of records")
            self.assertEqual(KNOWN_TITLES["A.8.10"], "Information deletion")
            r = assess_row("Some Document", ["A.5.33", "A.8.10"])
            self.assertIsNotNone(r)

        def test_no_dead_iso31000_titles_in_known_map(self):
            # M4 (P-1.83): ISO 31000 clause headings are deliberately NOT
            # code-matched (CODE_RE has no clause branch), so no "ISO 31000 §"
            # key may sit dead in KNOWN_TITLES. Guards against re-adding the
            # unreachable entries this fix removed.
            self.assertEqual(
                [k for k in KNOWN_TITLES if k.startswith("ISO 31000")], [],
                "ISO 31000 titles are unreachable via CODE_RE; do not add them to KNOWN_TITLES")

        def test_iso27001_only_row_anchored_rescued(self):
            # An ISO-only row whose control title shares a token with the subject
            # is rescued (anchored), same as any other assessable family.
            # A.8.13 = "Information backup" anchors a backup-standard subject.
            self.assertEqual(KNOWN_TITLES["A.8.13"], "Information backup")
            r = assess_row("Information Backup Standard", ["A.8.13", "A.8.14"])
            self.assertIsNone(r)

        def test_matrix_iso_column_extracted(self):
            # Regression (codex, P-1.62 I1): the matrix parser must READ the
            # "ISO/IEC 27001:2022" column, else the ISO title map is inert on the
            # matrix (codes are extracted per-column). A row whose only code is a
            # non-anchoring ISO control is assessed and flagged; before iso_idx
            # was wired the row was skipped (no assessable code found).
            m = (
                "| Domain | Document Title | Path | CSA CCM v4.1 "
                "| ISO/IEC 27001:2022 |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| Sec | Fire Suppression Plan | `sec/x.md` |  | A.5.1 |\n"
            )
            import tempfile, os
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(m); path = Path(f.name)
            try:
                cands, stats = scan_matrix(path)
                # A.5.1 = "Policies for information security" shares no token with
                # "Fire Suppression Plan" -> flagged, proving the ISO cell was read.
                self.assertEqual(stats["n_assessed"], 1)
                self.assertEqual(len(cands), 1)
                got = [c for c, _t, _o in cands[0]["codes"]]
                self.assertIn("A.5.1", got)
            finally:
                os.unlink(path)

        def test_aicm_only_code_is_assessable(self):
            # An AICM-only code (carried in the matrix's "CSA AICM v1.1" column)
            # now has a title via AICM_V11, so it participates in assessment.
            # MDS-02 = "Model Artifact Scanning" anchors a model-artifact subject
            # (shares "model"/"artifact") -> rescued, not flagged.
            self.assertIn("MDS-02", KNOWN_TITLES)
            self.assertEqual(KNOWN_TITLES["MDS-02"], "Model Artifact Scanning")
            r = assess_row("Model Artifact Integrity Verification", ["MDS-02"])
            self.assertIsNone(r)

        def test_aicm_only_code_no_anchor_flagged(self):
            # An AICM-only code whose title shares no token with the subject
            # lands the row on the worklist (recall-oriented), same as any other
            # assessable code with no lexical anchor. MDS-02 = "Model Artifact
            # Scanning" shares nothing with "Physical Perimeter Fencing".
            r = assess_row("Physical Perimeter Fencing", ["MDS-02"])
            self.assertIsNotNone(r)

        def test_prefix_token_match(self):
            self.assertTrue(token_match("classification", "classify"))
            self.assertTrue(token_match("retention", "retention"))
            self.assertFalse(token_match("data", "duty"))

        def test_parse_failure_on_reworded_matrix_header(self):
            # C4 (guard-inputs): a reworded/renamed header -> the anchor is never
            # matched -> 0 rows assessed. scan_matrix must report n_assessed == 0 so
            # report() refuses to assert a clean surface (PARSE-FAILURE), not "0 on
            # the worklist (every row has a lexical anchor)".
            import tempfile, os
            good = (
                "| Domain | Document Title | Path | CSA CCM v4.1 |\n"
                "| --- | --- | --- | --- |\n"
                "| Risk | Records Retention and Destruction | `x.md` | DSP-07 |\n"
                "| Risk | Third Party Risk | `y.md` | STA-01 |\n"
            )
            reworded = good.replace("CSA CCM v4.1", "CSA CCM (v4.1)")  # column renamed
            paths = []
            for body in (good, reworded):
                with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                    f.write(body); paths.append(Path(f.name))
            try:
                _, stats_good = scan_matrix(paths[0])
                _, stats_bad = scan_matrix(paths[1])
                self.assertEqual(stats_good["n_assessed"], 2,
                                 "a well-formed header must assess its data rows")
                self.assertEqual(stats_good["n_unparsed_tables"], 0,
                                 "a well-formed table has no unparsed tables")
                self.assertEqual(stats_bad["n_assessed"], 0,
                                 "a fully-reworded header must assess 0 rows (parse failure)")
                self.assertEqual(stats_bad["n_unassessable"], 0,
                                 "an unrecognized table's rows are never parsed, so they are "
                                 "not 'unassessable'; both zero is the PARSE-FAILURE signal")
            finally:
                for pth in paths:
                    os.unlink(pth)

        def test_partial_parse_flags_one_renamed_table(self):
            # codex HOLD (iter-1): the matrix has MANY mapping tables; renaming ONE
            # table's CCM column drops that table silently (n_assessed stays > 0). The
            # candidate-vs-recognized header count must surface it as n_unparsed > 0.
            import tempfile, os
            two_tables = (
                "| Domain | Document Title | Path | CSA CCM v4.1 |\n"
                "| --- | --- | --- | --- |\n"
                "| Risk | Third Party Risk | `y.md` | STA-01 |\n"
                "\n"
                "| Domain | Document Title | Path | CSA CCM (renamed) |\n"  # CCM col renamed
                "| --- | --- | --- | --- |\n"
                "| Ops | Media Handling | `m.md` | DCS-05 |\n"
            )
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(two_tables); path = Path(f.name)
            try:
                _, stats = scan_matrix(path)
                self.assertEqual(stats["n_assessed"], 1,
                                 "only the recognized table's row is assessed")
                self.assertEqual(stats["n_unparsed_tables"], 1,
                                 "the renamed-column table must be flagged unparsed")
            finally:
                os.unlink(path)

        def test_docs_scope_filters_matrix_rows(self):
            # --docs scoping: only rows whose Path cell is in the docs set are assessed.
            m = (
                "| Domain | Document Title | Path | CSA CCM v4.1 |\n"
                "| --- | --- | --- | --- |\n"
                "| Risk | Records Retention | `risk/a.md` | DSP-07 |\n"
                "| Ops | Media Handling | `ops/b.md` | DCS-05 |\n"
            )
            import tempfile, os
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(m); path = Path(f.name)
            try:
                _, stats_all = scan_matrix(path)
                _, stats_scoped = scan_matrix(path, {"risk/a.md"})
                self.assertEqual(stats_all["n_assessed"], 2)
                self.assertEqual(stats_scoped["n_assessed"], 1)
            finally:
                os.unlink(path)

        def test_json_output_is_valid(self):
            import io, contextlib, json as _json
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                run(matrix=True, source_docs=False,
                    docs=["compliance/matrix-grc-compliance-alignment.md"], as_json=True)
            d = _json.loads(buf.getvalue())
            self.assertIn("matrix", d)
            self.assertIn("worklist", d["matrix"])
            for key in ("n_unassessable", "unassessable", "unassessed_columns"):
                self.assertIn(key, d["matrix"])
            for entry in d["matrix"]["worklist"]:
                self.assertIn("unknown_codes", entry)

        def test_data_cell_named_document_title_is_not_a_candidate_header(self):
            # Hardening (claude/codex iter-2 note): a DATA cell whose value is literally
            # "Document Title" must NOT be counted as a candidate header (it lacks the
            # "Path" label column), so it cannot fire a spurious PARTIAL-PARSE warning.
            import tempfile, os
            body = (
                "| Domain | Document Title | Path | CSA CCM v4.1 |\n"
                "| --- | --- | --- | --- |\n"
                "| Ops | Document Title | `m.md` | DCS-05 |\n"  # data cell == 'Document Title'
            )
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(body); path = Path(f.name)
            try:
                _, stats = scan_matrix(path)
                self.assertEqual(stats["n_assessed"], 1)
                self.assertEqual(stats["n_unparsed_tables"], 0,
                                 "a data cell must not masquerade as a candidate header")
            finally:
                os.unlink(path)

        def test_report_flags_partial_parse(self):
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                report([], _stats(n_assessed=5, n_unparsed_tables=2), "Compliance matrix")
            out = buf.getvalue()
            self.assertIn("PARTIAL-PARSE WARNING", out)
            self.assertIn("2 mapping table(s)", out)

        def test_report_refuses_clean_on_parse_failure(self):
            # report() with n_assessed == 0 must print PARSE-FAILURE, never the
            # clean-state sentence.
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                report([], _stats(), "Compliance matrix")
            out = buf.getvalue()
            self.assertIn("PARSE-FAILURE", out)
            self.assertNotIn("has a lexical anchor", out)
            # and a genuine clean surface (rows assessed, none worklisted) still reads clean
            buf2 = io.StringIO()
            with contextlib.redirect_stdout(buf2):
                report([], _stats(n_assessed=42), "Compliance matrix")
            self.assertIn("assessed 42 row(s), 0 on the worklist", buf2.getvalue())

        def test_unknown_only_code_row_counted_unassessable(self):
            # M5 (P-1.83): a row whose only extracted code carries no held title
            # (a COBIT practice code; practice titles are deliberately absent
            # from COBIT_OBJECTIVES) is counted UNASSESSABLE and listed as the
            # judge's feeder, never folded into n_assessed (the prior shape
            # counted it assessed, assess_row returned None, and the row
            # silently backed the "every assessed row has a lexical anchor"
            # clean-line claim).
            self.assertNotIn("DSS05.03", KNOWN_TITLES)
            m = (
                "| Domain | Document Title | Path | CSA CCM v4.1 |\n"
                "| --- | --- | --- | --- |\n"
                "| Sec | Access Review Standard | `sec/x.md` | DSS05.03 |\n"
            )
            import tempfile, os
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(m); path = Path(f.name)
            try:
                cands, stats = scan_matrix(path)
                self.assertEqual(cands, [])
                self.assertEqual(stats["n_assessed"], 0)
                self.assertEqual(stats["n_unassessable"], 1)
                u = stats["unassessable"][0]
                self.assertTrue(u["location"].endswith(":3"), u["location"])
                self.assertEqual(u["subject"], "Access Review Standard")
                self.assertEqual(u["codes"], ["DSS05.03"])
            finally:
                os.unlink(path)

        def test_mixed_table_counts_and_qualified_clean_line(self):
            # M5: one anchored (assessable) row + one unknown-only row -> 1/1,
            # and the clean line is QUALIFIED (names the unassessable count)
            # instead of the bare every-row claim.
            m = (
                "| Domain | Document Title | Path | CSA CCM v4.1 |\n"
                "| --- | --- | --- | --- |\n"
                "| Risk | Records Retention and Destruction | `x.md` | DSP-16 |\n"
                "| Sec | Access Review Standard | `sec/x.md` | DSS05.03 |\n"
            )
            import tempfile, os, io, contextlib
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(m); path = Path(f.name)
            try:
                cands, stats = scan_matrix(path)
                self.assertEqual(stats["n_assessed"], 1)
                self.assertEqual(stats["n_unassessable"], 1)
                self.assertEqual(cands, [])  # DSP-16 anchors "Retention" -> off the worklist
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    report(cands, stats, "Compliance matrix")
                out = buf.getvalue()
                self.assertIn("1 row(s) not assessable", out)
                self.assertIn("not pre-filter-assessable", out)
                self.assertIn("DSS05.03", out)
            finally:
                os.unlink(path)

        def test_report_all_unassessable_is_not_parse_failure_and_not_clean(self):
            # M5: parsed-but-all-unassessable is its OWN honest line: NOT a
            # PARSE-FAILURE (the anchor matched, the rows were read) and NOT
            # the clean-state sentence.
            import io, contextlib
            rows = [
                dict(location="m.md:3", subject="Doc A", codes=["DSS05.03"]),
                dict(location="m.md:4", subject="Doc B", codes=["APO12.01"]),
            ]
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                report([], _stats(n_unassessable=2, unassessable=rows), "Compliance matrix")
            out = buf.getvalue()
            self.assertNotIn("PARSE-FAILURE", out)
            self.assertNotIn("has a lexical anchor", out)
            self.assertIn("not pre-filter-assessable", out)
            self.assertIn("NOT a clean result", out)
            self.assertIn("m.md:3", out)

        def test_worklisted_row_carries_unknown_codes(self):
            # M6 tool support: a worklisted row with a mixed known/unknown code
            # set carries the unknown codes (title-not-held candidates for the
            # judge), and report() prints them; an all-known worklisted row
            # carries an empty list.
            r = assess_row("Some Document", ["A.5.33", "DSS05.03"])
            self.assertIsNotNone(r)
            self.assertEqual(r["unknown_codes"], ["DSS05.03"])
            r2 = assess_row("Some Document", ["A.5.33"])
            self.assertIsNotNone(r2)
            self.assertEqual(r2["unknown_codes"], [])
            import io, contextlib
            r["location"] = "m.md:3"
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                report([r], _stats(n_assessed=1), "Compliance matrix")
            self.assertIn("title-not-held candidates", buf.getvalue())

        def test_row_assessable_helper(self):
            # M5: the assessability predicate itself.
            self.assertTrue(row_assessable("Records Retention", ["DSP-16"]))
            self.assertFalse(row_assessable("Records Retention", ["DSS05.03"]))
            self.assertFalse(row_assessable("Records Retention", []))
            self.assertFalse(row_assessable("", ["DSP-16"]))

        def test_unassessed_columns_advisory(self):
            # M3 (P-1.83): framework columns in a recognized header with no
            # wired title map (the sector columns) accumulate into
            # stats["unassessed_columns"] and print as an ADVISORY, instead of
            # silently vanishing from the counts.
            m = (
                "| Domain | Document Title | Path | CSA CCM v4.1 | CTPAT | WCO SAFE |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| Risk | Records Retention and Destruction | `x.md` | DSP-16 | 5.1 | Pillar 2 |\n"
            )
            import tempfile, os, io, contextlib
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(m); path = Path(f.name)
            try:
                cands, stats = scan_matrix(path)
                self.assertEqual(stats["unassessed_columns"], ["CTPAT", "WCO SAFE"])
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    report(cands, stats, "Compliance matrix")
                out = buf.getvalue()
                self.assertIn("ADVISORY", out)
                self.assertIn("CTPAT, WCO SAFE", out)
            finally:
                os.unlink(path)

        def test_scan_source_docs_stats_shape_on_live_corpus(self):
            # codex PR-A coverage gap: exercise scan_source_docs's new stats shape
            # (M5) on the real corpus - the same-shape refactor as scan_matrix, so
            # a shape regression here (missing key, wrong type) is caught.
            cands, stats = scan_source_docs()
            for key in ("n_assessed", "n_unassessable", "n_unparsed_tables",
                        "unassessable", "unassessed_columns"):
                self.assertIn(key, stats)
            self.assertEqual(stats["unassessed_columns"], [],
                             "source-doc framework identity is per-row, not a header column")
            self.assertEqual(stats["n_unparsed_tables"], 0,
                             "source docs are per-doc: no multi-table partial case")
            self.assertIsInstance(stats["unassessable"], list)
            self.assertGreater(stats["n_assessed"], 0, "the live corpus has assessable source docs")


        def test_recognized_header_without_path_never_negative_unparsed(self):
            # P-1.85: a recognized mapping table lacking a "Path" column is
            # recognized but not a candidate; the direct |candidate \\ recognized|
            # count must simply not include it (0 here), and can never go negative.
            m = (
                "| Domain | Document Title | CSA CCM v4.1 |\n"   # recognized, NO Path column
                "| --- | --- | --- |\n"
                "| Risk | Records Retention and Destruction | DSP-16 |\n"
            )
            import tempfile, os
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(m); path = Path(f.name)
            try:
                _, stats = scan_matrix(path)
                self.assertGreaterEqual(stats["n_unparsed_tables"], 0,
                                        "a Path-less recognized header must not drive n_unparsed negative")
                self.assertEqual(stats["n_unparsed_tables"], 0)
            finally:
                os.unlink(path)


        def test_unparsed_count_not_cancelled_by_pathless_recognized_table(self):
            # P-1.85 (panel r2): the count must be |candidate \ recognized|, NOT
            # max(0, |candidate| - |recognized|). A file with BOTH a genuinely
            # unparsed table (Document Title + Path, but a renamed CSA column) AND
            # a Path-less recognized table (recognized, not candidate) would, under
            # the aggregate-subtraction clamp, net to 0 and MASK the real unparsed
            # table. The direct per-header count reports it correctly as 1.
            m = (
                "| Domain | Document Title | Path | CSA CCM (renamed) |\n"   # candidate, CCM renamed -> UNPARSED
                "| --- | --- | --- | --- |\n"
                "| Ops | Media Handling | `m.md` | DCS-05 |\n"
                "\n"
                "| Domain | Document Title | CSA CCM v4.1 |\n"               # recognized, NO Path
                "| --- | --- | --- |\n"
                "| Risk | Records Retention | DSP-16 |\n"
            )
            import tempfile, os
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
                f.write(m); path = Path(f.name)
            try:
                _, stats = scan_matrix(path)
                self.assertEqual(stats["n_unparsed_tables"], 1,
                                 "the genuine renamed-CCM table must be counted, not cancelled "
                                 "by the Path-less recognized table")
            finally:
                os.unlink(path)


        def test_source_doc_worklist_locations_carry_line_numbers(self):
            # P-1.83 N4: source-doc worklist entries cite path:line (the framework-
            # alignment section heading line), uniform with the matrix surface,
            # instead of a bare path. Every source-doc worklist location must end
            # in ":<digits>".
            cands, _ = scan_source_docs()
            for c in cands:
                loc = c["location"]
                self.assertIn(":", loc, loc)
                self.assertTrue(loc.rsplit(":", 1)[1].isdigit(),
                                f"source-doc location must end in :<line>, got {loc!r}")


    suite = unittest.TestLoader().loadTestsFromTestCase(SemanticFitTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Advisory matrix/source-doc semantic-fit pre-filter (not a gate).")
    parser.add_argument("--matrix-only", action="store_true", help="scan only the compliance matrix")
    parser.add_argument("--source-docs-only", action="store_true", help="scan only source-doc framework tables")
    parser.add_argument("--self-test", action="store_true", help="run the inline unit tests and exit")
    parser.add_argument("--docs", nargs="+", metavar="PATH",
                        help="scope to matrix rows / source docs whose path is in this set (per-batch cadence)")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="emit the worklist as JSON (for a dispatch brief or a run-over-run diff)")
    args = parser.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    matrix = not args.source_docs_only
    source_docs = not args.matrix_only
    return run(matrix, source_docs, docs=args.docs, as_json=args.as_json)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
