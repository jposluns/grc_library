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
categories via ``CSF_CATEGORIES``), NO control's title shares a
single significant word with the document subject. A single anchoring code (a
sibling whose title overlaps the subject) keeps the row OFF the worklist, both
because matrix rows legitimately carry a primary mapping plus looser supporting
codes and because the goal is to narrow the semantic audit's scope, not to
adjudicate. The subtler "loose supporting code on an otherwise-anchored row"
case (e.g. matrix row 163's TVM-06 on a pen-testing standard, Sweep-61 note
A-note-1) is intentionally NOT on the worklist: an anchored row is deprioritized,
and that residual case is exactly what the semantic `/matrix-fit` skill catches.
ISO/IEC 27001:2022 codes are not assessed (no Annex A title source in the repo;
ISO 31000 clause headings and COBIT 2019 objective titles ARE assessable since
the 2026-07-02 cobit_iso31000_reference extension); rows whose
only known-title codes are absent are skipped (not assessable, so not listed).

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
from cobit_iso31000_reference import COBIT_OBJECTIVES, ISO31000_CLAUSES
from nist_csf_reference import CSF_CATEGORIES

try:
    from lint_common import AUDITED_DOMAIN_DIRS
except Exception:  # pragma: no cover - lint_common shape is stable; fallback keeps the aid runnable
    AUDITED_DOMAIN_DIRS = (
        "ai", "architecture", "compliance", "dev-security", "governance",
        "operations", "privacy", "resilience", "risk", "security", "supply-chain",
    )

REPO_ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = REPO_ROOT / "compliance" / "matrix-grc-compliance-alignment.md"

# Combined code -> title lookup the aid can assess against (CCM v4.1 + AICM v1.1
# + CSF 2.0 categories). ISO codes have no title source and are intentionally
# absent. AICM v1.1 is the AI-focused extension of CCM v4.1; as an implementation
# detail its code-set carries the CCM base plus 40 AICM-only codes (identical
# titles for the shared base). Updating AICM_V11 folds in the AICM-only titles so
# the matrix's "CSA AICM v1.1" column (which carries those AICM-only codes) is
# assessable; the shared-base titles are unchanged by the update.
KNOWN_TITLES: dict[str, str] = {}
KNOWN_TITLES.update(CCM_V41)
KNOWN_TITLES.update(AICM_V11)
KNOWN_TITLES.update(CSF_CATEGORIES)
# COBIT 2019 objective titles and ISO 31000:2018 clause headings (the
# 2026-07-02 extension; gate-blind fit judgment for the two families gates
# 48/49/54/58 do not cover, per the PR #587 build). Practice-level COBIT
# titles are deliberately absent from the reference module (extraction wraps
# them), so practice codes are existence-checked by the companion gate and
# fit-assessed here only at the objective level.
KNOWN_TITLES.update(COBIT_OBJECTIVES)
KNOWN_TITLES.update(
    {f"ISO 31000 §{k}": v for k, v in ISO31000_CLAUSES.items()})

# Control-code token: CCM (e.g. DSP-16, A&A-02), CSF category (e.g. GV.OC),
# or a COBIT 2019 objective/practice code (e.g. APO12, DSS05.03; practice
# codes are collected so the row surfaces on the worklist, though only the
# objective level carries a known title for the overlap heuristic).
CODE_RE = re.compile(
    r"\b(?:[A-Z&]{2,4}-[0-9]{2}|(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}"
    r"|(?:EDM|APO|BAI|DSS|MEA)\d{2}(?:\.\d{2})?)\b")

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
    judgement that the row is wrong.
    """
    subject = significant_tokens(subject_text)
    if not subject:
        return None
    known = [(c, KNOWN_TITLES[c]) for c in codes if c in KNOWN_TITLES]
    if not known:
        return None  # nothing assessable (e.g. ISO-only) -> do not flag
    best = 0
    per_code = []
    for code, title in known:
        score = overlap_count(subject, significant_tokens(title))
        per_code.append((code, title, score))
        best = max(best, score)
    if best == 0:
        return {"subject": subject_text, "codes": per_code}
    return None


# --- Matrix parsing ---------------------------------------------------------

def _split_row(line: str) -> list[str]:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def scan_matrix(path: Path, docs=None) -> tuple[list[dict], int, int]:
    """Scan the compliance matrix's per-domain mapping tables.

    Returns (candidates, n_assessed, n_unparsed_tables). n_assessed is the number of data
    rows actually read; n_unparsed_tables is the count of "Document Title"+"Path" header
    rows whose "CSA CCM v4.1" column was renamed (a table silently skipped, a PARTIAL parse
    failure). n_assessed == 0 means the header anchor was
    never matched (a reworded/renamed column), i.e. a PARSE FAILURE, NOT a clean
    surface: the caller must refuse to assert cleanliness in that case (guard-inputs
    discipline; make ignorance a first-class return that refuses rather than permits).
    """
    candidates: list[dict] = []
    n_assessed = 0
    n_candidate_headers = 0  # rows that look like a mapping-table header ("Document Title" present)
    n_recognized_headers = 0  # of those, the ones whose "CSA CCM v4.1" column was also found
    lines = path.read_text(encoding="utf-8").splitlines()
    title_idx = ccm_idx = aicm_idx = csf_idx = cobit_idx = path_idx = None
    in_table = False
    for raw, line in enumerate(lines, start=1):
        if line.lstrip().startswith("|"):
            cells = _split_row(line)
            # A candidate mapping-table header carries BOTH stable label columns
            # ("Document Title" and "Path"); requiring both stops a lone data cell whose
            # value is literally "Document Title" from masquerading as a header.
            if "Document Title" in cells and "Path" in cells:
                n_candidate_headers += 1
            # Header row of a mapping table?
            if "Document Title" in cells and "CSA CCM v4.1" in cells:
                n_recognized_headers += 1
                title_idx = cells.index("Document Title")
                ccm_idx = cells.index("CSA CCM v4.1")
                aicm_idx = cells.index("CSA AICM v1.1") if "CSA AICM v1.1" in cells else None
                csf_idx = cells.index("NIST CSF 2.0") if "NIST CSF 2.0" in cells else None
                cobit_idx = cells.index("COBIT 2019") if "COBIT 2019" in cells else None
                path_idx = cells.index("Path") if "Path" in cells else None
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
            n_assessed += 1
            result = assess_row(subject, codes)
            if result:
                try:
                    rel = path.relative_to(REPO_ROOT)
                except ValueError:  # a path outside the repo (e.g. a self-test temp file)
                    rel = path
                result["location"] = f"{rel}:{raw}"
                candidates.append(result)
        else:
            in_table = False
            title_idx = ccm_idx = aicm_idx = csf_idx = cobit_idx = path_idx = None
    # A "Document Title" header row whose "CSA CCM v4.1" column was renamed is a table
    # the scan silently skipped (a PARTIAL parse failure). Residue: a table whose
    # "Document Title" column itself was renamed is invisible to this candidate count.
    n_unparsed_tables = n_candidate_headers - n_recognized_headers
    return candidates, n_assessed, n_unparsed_tables


# --- Source-doc framework-table parsing -------------------------------------

FRAMEWORK_HEADING_RE = re.compile(r"^#{2,3}\s.*framework alignment", re.IGNORECASE)
H1_RE = re.compile(r"^#\s+(.*\S)\s*$")


def _doc_title(lines: list[str]) -> str | None:
    for line in lines:
        m = H1_RE.match(line)
        if m:
            return m.group(1).strip()
    return None


def scan_source_doc(path: Path) -> tuple[dict | None, bool]:
    """Scan one corpus document's '## Framework alignment' table, if present."""
    lines = path.read_text(encoding="utf-8").splitlines()
    subject = _doc_title(lines)
    if not subject:
        return None, False
    # Locate the framework-alignment section and collect codes from its table.
    in_section = False
    codes: list[str] = []
    for line in lines:
        if line.startswith("#"):
            in_section = bool(FRAMEWORK_HEADING_RE.match(line))
            continue
        if in_section and line.lstrip().startswith("|"):
            codes += CODE_RE.findall(line)
    if not codes:
        return None, False
    result = assess_row(subject, codes)
    if result:
        try:
            result["location"] = f"{path.relative_to(REPO_ROOT)}"
        except ValueError:
            result["location"] = f"{path}"
    return result, True


def scan_source_docs(docs=None) -> tuple[list[dict], int, int]:
    """Scan every corpus document's framework-alignment table. Recurses into domain
    SUBDIRECTORIES (sector annexes under compliance/<sector>/, jurisdiction annexes
    under ai/jurisdictions/, ...) via rglob, matching the docstring's "each corpus
    document" claim. Returns (candidates, n_assessed, n_unparsed) where n_assessed counts
    docs that carried a framework-alignment table (0 assessed is a PARSE FAILURE, not a
    clean result); n_unparsed is always 0 here (source docs are per-doc, no multi-table)."""
    candidates: list[dict] = []
    n_assessed = 0
    for domain in AUDITED_DOMAIN_DIRS:
        d = REPO_ROOT / domain
        if not d.is_dir():
            continue
        for md in sorted(d.rglob("*.md")):
            if md.resolve() == MATRIX_PATH.resolve():
                continue
            if docs is not None and md.relative_to(REPO_ROOT).as_posix() not in docs:
                continue
            res, had_table = scan_source_doc(md)
            if had_table:
                n_assessed += 1
            if res:
                candidates.append(res)
    return candidates, n_assessed, 0  # source docs are per-doc: no multi-table partial case


# --- Reporting --------------------------------------------------------------

def report(candidates: list[dict], n_assessed: int, surface: str, n_unparsed: int = 0) -> None:
    if n_assessed == 0:
        print(f"  {surface}: PARSE-FAILURE - 0 rows assessed. The header/table anchor was "
              f"NOT found (a renamed or reworded column), so the scan could not read this "
              f"surface. This is NOT a clean result; do not trust the worklist as empty.")
        return
    if n_unparsed > 0:
        print(f"  {surface}: PARTIAL-PARSE WARNING - {n_unparsed} mapping table(s) had a "
              f"'Document Title' header but no recognized 'CSA CCM v4.1' column (a renamed "
              f"column), so those tables were SKIPPED. The worklist below is INCOMPLETE.")
    if not candidates:
        print(f"  {surface}: assessed {n_assessed} row(s), 0 on the worklist "
              f"(every assessed row has a lexical anchor).")
        return
    print(f"  {surface}: assessed {n_assessed} row(s), {len(candidates)} on the semantic-audit worklist:")
    for c in candidates:
        print(f"    - {c['location']}  subject: {c['subject']!r}")
        for code, title, score in c["codes"]:
            print(f"        {code} = {title!r} (overlap {score})")


def run(matrix: bool, source_docs: bool, docs=None, as_json=False) -> int:
    docset = None if docs is None else {str(Path(d).as_posix()) for d in docs}
    if as_json:
        import json as _json
        out = {"scoped_docs": (sorted(docset) if docset is not None else None)}
        def _wl(cands):
            return [{"location": c["location"], "subject": c["subject"],
                     "codes": [{"code": code, "title": title, "overlap": score}
                               for code, title, score in c["codes"]]} for c in cands]
        if matrix:
            cands, n, nu = scan_matrix(MATRIX_PATH, docset)
            out["matrix"] = {"assessed": n, "n_unparsed_tables": nu, "worklist": _wl(cands)}
        if source_docs:
            cands, n, nu = scan_source_docs(docset)
            out["source_docs"] = {"assessed": n, "worklist": _wl(cands)}
        print(_json.dumps(out, indent=2))
        return 0
    print("ADVISORY semantic-fit TRIAGE worklist for the /matrix-fit audit (NOT a gate; exit 0 always).")
    print("Listed rows lack a lexical anchor; they are the audit's worklist, NOT confirmed defects.")
    print("Non-listed rows are deprioritized, NOT certified; the /matrix-fit skill adjudicates fit.\n")
    if matrix:
        cands, n, n_unparsed = scan_matrix(MATRIX_PATH, docset)
        report(cands, n, "Compliance matrix", n_unparsed)
    if source_docs:
        cands, n, n_unparsed = scan_source_docs(docset)
        report(cands, n, "Source-doc framework tables", n_unparsed)
    print(
        "\nThe /matrix-fit semantic audit judges each listed row against the source control "
        "TITLE (CCM v4.1 / AICM v1.1 / CSF 2.0 / COBIT 2019 / ISO 31000:2018). A "
        "worklisted row is a focus candidate, not a "
        "mismatch; a non-worklisted row may still carry a loose supporting code (the skill covers those too)."
    )
    return 0


# --- Inline self-test (kept out of tests/ so gate 36 does not adopt it) ------

def _self_test() -> int:
    import unittest

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

        def test_iso_only_row_skipped(self):
            # No known-title codes (ISO has no title source) -> not flagged.
            r = assess_row("Some Document", ["A.5.33", "A.8.10"])
            self.assertIsNone(r)

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
                _, n_good, unparsed_good = scan_matrix(paths[0])
                _, n_bad, _ = scan_matrix(paths[1])
                self.assertEqual(n_good, 2, "a well-formed header must assess its data rows")
                self.assertEqual(unparsed_good, 0, "a well-formed table has no unparsed tables")
                self.assertEqual(n_bad, 0, "a fully-reworded header must assess 0 rows (parse failure)")
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
                _, n_assessed, n_unparsed = scan_matrix(path)
                self.assertEqual(n_assessed, 1, "only the recognized table's row is assessed")
                self.assertEqual(n_unparsed, 1, "the renamed-column table must be flagged unparsed")
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
                _, n_all, _ = scan_matrix(path)
                _, n_scoped, _ = scan_matrix(path, {"risk/a.md"})
                self.assertEqual(n_all, 2)
                self.assertEqual(n_scoped, 1)
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
                _, n_assessed, n_unparsed = scan_matrix(path)
                self.assertEqual(n_assessed, 1)
                self.assertEqual(n_unparsed, 0, "a data cell must not masquerade as a candidate header")
            finally:
                os.unlink(path)

        def test_report_flags_partial_parse(self):
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                report([], 5, "Compliance matrix", n_unparsed=2)
            out = buf.getvalue()
            self.assertIn("PARTIAL-PARSE WARNING", out)
            self.assertIn("2 mapping table(s)", out)

        def test_report_refuses_clean_on_parse_failure(self):
            # report() with n_assessed == 0 must print PARSE-FAILURE, never the
            # clean-state sentence.
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                report([], 0, "Compliance matrix")
            out = buf.getvalue()
            self.assertIn("PARSE-FAILURE", out)
            self.assertNotIn("has a lexical anchor", out)
            # and a genuine clean surface (rows assessed, none worklisted) still reads clean
            buf2 = io.StringIO()
            with contextlib.redirect_stdout(buf2):
                report([], 42, "Compliance matrix")
            self.assertIn("assessed 42 row(s), 0 on the worklist", buf2.getvalue())

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
