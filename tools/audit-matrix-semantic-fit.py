#!/usr/bin/env python3
"""Advisory semantic-fit pre-filter for the compliance matrix and source-doc
framework tables (the gate-blind "valid code, wrong control" class).

WHAT THIS IS (and is NOT). This is a maintainer dev-AID, not an audit gate. The
audit gates 48/49/54 check that a cited control code EXISTS in its framework
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
NIST CSF 2.0 categories via ``CSF_CATEGORIES``), NO control's title shares a
single significant word with the document subject. A single anchoring code (a
sibling whose title overlaps the subject) keeps the row OFF the worklist, both
because matrix rows legitimately carry a primary mapping plus looser supporting
codes and because the goal is to narrow the semantic audit's scope, not to
adjudicate. The subtler "loose supporting code on an otherwise-anchored row"
case (e.g. matrix row 163's TVM-06 on a pen-testing standard, Sweep-61 note
A-note-1) is intentionally NOT on the worklist: an anchored row is deprioritized,
and that residual case is exactly what the semantic `/matrix-fit` skill catches.
ISO 27001:2022 codes are not assessed (no title source in the repo); rows whose
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

from ccm_aicm_reference import CCM_V41
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

# Combined code -> title lookup the aid can assess against (CCM v4.1 + CSF 2.0
# categories). ISO codes have no title source and are intentionally absent.
KNOWN_TITLES: dict[str, str] = {}
KNOWN_TITLES.update(CCM_V41)
KNOWN_TITLES.update(CSF_CATEGORIES)

# Control-code token: CCM (e.g. DSP-16, A&A-02) or CSF category (e.g. GV.OC).
CODE_RE = re.compile(r"\b(?:[A-Z&]{2,4}-[0-9]{2}|(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2})\b")

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


def scan_matrix(path: Path) -> list[dict]:
    """Scan the compliance matrix's per-domain mapping tables."""
    candidates: list[dict] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    title_idx = ccm_idx = csf_idx = None
    in_table = False
    for raw, line in enumerate(lines, start=1):
        if line.lstrip().startswith("|"):
            cells = _split_row(line)
            # Header row of a mapping table?
            if "Document Title" in cells and "CSA CCM v4.1" in cells:
                title_idx = cells.index("Document Title")
                ccm_idx = cells.index("CSA CCM v4.1")
                csf_idx = cells.index("NIST CSF 2.0") if "NIST CSF 2.0" in cells else None
                in_table = True
                continue
            if not in_table or title_idx is None:
                continue
            if set(cells) <= {"", "---"} or all(set(c) <= {"-"} for c in cells if c):
                continue  # separator row
            if len(cells) <= ccm_idx:
                continue
            subject = strip_type_prefix(cells[title_idx])
            codes = CODE_RE.findall(cells[ccm_idx])
            if csf_idx is not None and len(cells) > csf_idx:
                codes += CODE_RE.findall(cells[csf_idx])
            result = assess_row(subject, codes)
            if result:
                result["location"] = f"{path.relative_to(REPO_ROOT)}:{raw}"
                candidates.append(result)
        else:
            in_table = False
            title_idx = ccm_idx = csf_idx = None
    return candidates


# --- Source-doc framework-table parsing -------------------------------------

FRAMEWORK_HEADING_RE = re.compile(r"^#{2,3}\s.*framework alignment", re.IGNORECASE)
H1_RE = re.compile(r"^#\s+(.*\S)\s*$")


def _doc_title(lines: list[str]) -> str | None:
    for line in lines:
        m = H1_RE.match(line)
        if m:
            return m.group(1).strip()
    return None


def scan_source_doc(path: Path) -> dict | None:
    """Scan one corpus document's '## Framework alignment' table, if present."""
    lines = path.read_text(encoding="utf-8").splitlines()
    subject = _doc_title(lines)
    if not subject:
        return None
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
        return None
    result = assess_row(subject, codes)
    if result:
        result["location"] = f"{path.relative_to(REPO_ROOT)}"
    return result


def scan_source_docs() -> list[dict]:
    candidates: list[dict] = []
    for domain in AUDITED_DOMAIN_DIRS:
        d = REPO_ROOT / domain
        if not d.is_dir():
            continue
        for md in sorted(d.glob("*.md")):
            if md.resolve() == MATRIX_PATH.resolve():
                continue
            res = scan_source_doc(md)
            if res:
                candidates.append(res)
    return candidates


# --- Reporting --------------------------------------------------------------

def report(candidates: list[dict], surface: str) -> None:
    if not candidates:
        print(f"  {surface}: 0 rows on the worklist (every row has a lexical anchor).")
        return
    print(f"  {surface}: {len(candidates)} row(s) on the semantic-audit worklist:")
    for c in candidates:
        print(f"    - {c['location']}  subject: {c['subject']!r}")
        for code, title, score in c["codes"]:
            print(f"        {code} = {title!r} (overlap {score})")


def run(matrix: bool, source_docs: bool) -> int:
    print("ADVISORY semantic-fit TRIAGE worklist for the /matrix-fit audit (NOT a gate; exit 0 always).")
    print("Listed rows lack a lexical anchor; they are the audit's worklist, NOT confirmed defects.")
    print("Non-listed rows are deprioritized, NOT certified; the /matrix-fit skill adjudicates fit.\n")
    if matrix:
        report(scan_matrix(MATRIX_PATH), "Compliance matrix")
    if source_docs:
        report(scan_source_docs(), "Source-doc framework tables")
    print(
        "\nThe /matrix-fit semantic audit judges each listed row against the source control "
        "TITLE (CCM v4.1 / CSF 2.0). A worklisted row is a focus candidate, not a mismatch; "
        "a non-worklisted row may still carry a loose supporting code (the skill covers those too)."
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

        def test_prefix_token_match(self):
            self.assertTrue(token_match("classification", "classify"))
            self.assertTrue(token_match("retention", "retention"))
            self.assertFalse(token_match("data", "duty"))

    suite = unittest.TestLoader().loadTestsFromTestCase(SemanticFitTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Advisory matrix/source-doc semantic-fit pre-filter (not a gate).")
    parser.add_argument("--matrix-only", action="store_true", help="scan only the compliance matrix")
    parser.add_argument("--source-docs-only", action="store_true", help="scan only source-doc framework tables")
    parser.add_argument("--self-test", action="store_true", help="run the inline unit tests and exit")
    args = parser.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    matrix = not args.source_docs_only
    source_docs = not args.matrix_only
    return run(matrix, source_docs)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
