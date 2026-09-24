#!/usr/bin/env python3
"""Narrative metadata gate (P-1.25 Phase 1.2).

Validates every executive narrative page under the root ``executive/`` tree
against the Executive Narrative Authoring Specification
(``specification-executive-narrative.md``). This is the ``narrative-only`` gate
family's metadata member: unlike the corpus metadata gate (which EXCLUDES
``executive/``), this gate scans ONLY ``executive/`` and requires narrative-page
form on every page, with a single named exemption for the entry point
``executive/README.md`` (the hand-curated concern-framing README, not a
narrative page; per the spec's placement/entry-point exemption).

Checks per narrative page:
  - Document Type is exactly ``Executive Narrative``.
  - The 13 canonical fields are present, in canonical order.
  - The 8 narrative-extension fields are present, in order, after ``License``.
  - ``Narrative Type`` is one of the seven closed subtypes.
  - ``Narrative Status`` is one of the three closed values AND matches the fixed
    subtype-to-status mapping.
  - The filename prefix matches the ``Narrative Type``'s mandatory prefix.
  - The page lives in the subtype's mandatory subdirectory under ``executive/``.
  - At least one ``Corpus Sources`` pin, each a plain markdown link to the corpus
    document (a path reference, no version suffix), with a single pin per target
    (no duplicate pin on the same target).
  - Body-link/pin completeness: every corpus document linked in the page body
    appears in ``Corpus Sources``.
  - Backslash hard-break markers on every metadata line except the block's last.
  - ``Claim Classes Present`` is a subset of the closed vocabulary (citation,
    sourced, composite); ``Last Reviewed`` is a valid ISO 8601 date.

Exit 0 if every narrative page is valid (an executive/ tree holding only the
entry-point README is valid: zero pages, zero findings). Exit 1 on any finding.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import REPO_ROOT, guard_explicit_paths_cwd, is_narrative_root  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

NARRATIVE_DOCUMENT_TYPE = "Executive Narrative"
ENTRY_POINT = "executive/README.md"

CANONICAL_FIELDS: list[str] = [
    "Document Title",
    "Document Type",
    "Version",
    "Date",
    "Owner",
    "Approving Authority",
    "Related Documents",
    "Classification",
    "Category",
    "Review Frequency",
    "Repository Path",
    "Confidentiality",
    "License",
]

EXTENSION_FIELDS: list[str] = [
    "Narrative Type",
    "Narrative Status",
    "Audience",
    "Corpus Sources",
    "External Sources",
    "Claim Classes Present",
    "Review Record",
    "Last Reviewed",
]

SUBTYPES: dict[str, tuple[str, str, str]] = {
    "Executive Brief": ("brief-", "Explanatory", "briefs"),
    "Scenario": ("scenario-", "Non-normative", "scenarios"),
    "Decision Narrative": ("decision-", "Advisory", "decision-narratives"),
    "Oversight Question Set": ("oversight-questions-", "Advisory", "oversight-question-sets"),
    "Story": ("story-", "Non-normative", "stories"),
    "Journey": ("journey-", "Explanatory", "journeys"),
    "Outcome Map": ("outcome-map-", "Explanatory", "outcome-maps"),
}

STATUSES: frozenset[str] = frozenset({"Non-normative", "Advisory", "Explanatory"})

CORPUS_DOMAIN_PREFIXES = (
    "ai/", "architecture/", "compliance/", "crypto/", "dev-security/", "governance/",
    "operations/", "privacy/", "resilience/", "risk/", "security/", "supply-chain/",
)

ROOT_CORPUS_DOCS = frozenset({
    "README.md", "NOTICE.md", "specification-master-project.md",
    "specification-ingestion.md", "specification-executive-narrative.md",
    "instruction-ai-document-ingestion.md",
})

CLAIM_CLASSES = frozenset({"citation", "sourced", "composite"})


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_narrative_metadata  # the pack-owned engine (source of record)
    return gate_lint_narrative_metadata


# Configure the engine ONCE with the grc project-content sets + repo root.
import types  # noqa: E402
_engine().configure(types.SimpleNamespace(
    narrative_document_type=NARRATIVE_DOCUMENT_TYPE, entry_point=ENTRY_POINT,
    canonical_fields=CANONICAL_FIELDS, extension_fields=EXTENSION_FIELDS, subtypes=SUBTYPES,
    statuses=STATUSES, corpus_domain_prefixes=CORPUS_DOMAIN_PREFIXES,
    root_corpus_docs=ROOT_CORPUS_DOCS, claim_classes=CLAIM_CLASSES, repo_root=REPO_ROOT))


def audit_page(path: Path) -> list[str]:
    """Shim -> engine (engine already configured); kept module-global for the self-test + main."""
    return _engine().audit_page(path)


def discover_pages() -> list[Path]:
    exec_root = REPO_ROOT / "executive"
    if not exec_root.is_dir():
        return []
    pages: list[Path] = []
    for p in sorted(exec_root.rglob("*.md")):
        if not is_narrative_root(p):
            continue
        if p.relative_to(REPO_ROOT).as_posix() == ENTRY_POINT:
            continue  # the single named entry-point exemption
        pages.append(p)
    return pages


def _self_test() -> int:
    """Exercise the gate against synthetic per-failure-class pages (a valid page plus a case per
    known failure class), so the
    gate's detection logic is proven even while the live ``executive/`` tree holds
    only the exempted entry-point README (zero real pages). Mirrors gate 82's
    self-test discipline. Returns 0 iff every case behaves as expected."""
    import tempfile

    valid = """# AI Risk Appetite Decision

**Document Title:** AI Risk Appetite Decision\\
**Document Type:** Executive Narrative\\
**Version:** 0.0.1\\
**Date:** 2026-08-05\\
**Owner:** Governance Library Maintainer\\
**Approving Authority:** Governance Library Maintainer\\
**Related Documents:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\\
**Classification:** Public\\
**Category:** Executive Narrative\\
**Review Frequency:** Annual\\
**Repository Path:** [`executive/decision-narratives/decision-ai-risk-appetite.md`](decision-ai-risk-appetite.md)\\
**Confidentiality:** Public\\
**License:** CC BY-SA 4.0\\
**Narrative Type:** Decision Narrative\\
**Narrative Status:** Advisory\\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\\
**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\\
**External Sources:** None\\
**Claim Classes Present:** citation\\
**Review Record:** NR-2026-001\\
**Last Reviewed:** 2026-08-05

---

Body cites [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md).
"""
    # (filename, transform, expected substring in a finding, or None to expect PASS)
    cases: list[tuple[str, str, str | None]] = [
        ("decision-valid.md", valid, None),
        ("decision-badtype.md", valid.replace("**Document Type:** Executive Narrative", "**Document Type:** Guide"), "Document Type must be"),
        ("decision-nocanon.md", valid.replace("**Owner:** Governance Library Maintainer\\\n", ""), "missing canonical field: Owner"),
        ("decision-noext.md", valid.replace("**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\\\n", ""), "missing narrative-extension field: Audience"),
        ("decision-badntype.md", valid.replace("**Narrative Type:** Decision Narrative", "**Narrative Type:** Bogus Type"), "not one of the seven closed subtypes"),
        ("decision-badstatus.md", valid.replace("**Narrative Status:** Advisory", "**Narrative Status:** Explanatory"), "does not match the fixed status"),
        ("decision-badvocab.md", valid.replace("**Narrative Status:** Advisory", "**Narrative Status:** Bogus"), "not one of"),
        ("decision-outoforder.md", valid.replace("**Version:** 0.0.1\\\n**Date:** 2026-08-05\\\n", "**Date:** 2026-08-05\\\n**Version:** 0.0.1\\\n"), "out of canonical order"),
        ("decision-malformedpin.md", valid.replace("(../../risk/annex-ai-risk-methodology.md)\\", "(../../risk/annex-ai-risk-methodology.md)@1.0.6\\"), "malformed Corpus Sources pin"),
        ("decision-hiddenmalformed.md", valid.replace("[`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\\", "[`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md) [`governance/charter-governance-library.md`](../../governance/charter-governance-library.md)@2.0.0\\"), "malformed Corpus Sources pin"),
        ("decision-aliasdup.md", valid.replace("**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)", "**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md), [`risk/annex-ai-risk-methodology.md`](risk/annex-ai-risk-methodology.md)"), "duplicate Corpus Sources pin"),
        ("decision-lastbackslash.md", valid.replace("**Last Reviewed:** 2026-08-05", "**Last Reviewed:** 2026-08-05\\"), "last metadata line must be bare"),
        ("decision-interposed.md", valid.replace("**License:** CC BY-SA 4.0\\", "**License:** CC BY-SA 4.0\\\n**Bogus Field:** x\\"), "unexpected metadata field"),
        ("wrongprefix.md", valid, "filename must start with"),
        ("decision-nopin.md", re.sub(r"\*\*Corpus Sources:\*\*.*", "**Corpus Sources:** none\\\\", valid), "at least one pin"),
        ("decision-noncorpuspin.md", valid.replace("[`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\\\n**External Sources:**", "[`executive/README.md`](README.md)\\\n**External Sources:**"), "is not a corpus document"),
        ("decision-traversalpin.md", valid.replace("[`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\\\n**External Sources:**", "[`risk/annex-ai-risk-methodology.md`](../../risk/../executive/x.md)\\\n**External Sources:**"), "is not a corpus document"),
        ("decision-encodedpin.md", valid.replace("[`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\\\n**External Sources:**", "[`risk/annex-ai-risk-methodology.md`](../../risk/%2e%2e/executive/x.md)\\\n**External Sources:**"), "is not a corpus document"),
        ("decision-duppin.md", valid.replace("**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)", "**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md), [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)"), "duplicate Corpus Sources pin"),
        ("decision-unpinnedbody.md", valid.replace("Body cites [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md).", "Body links [`governance/charter-governance-library.md`](../../governance/charter-governance-library.md)."), "not present in Corpus Sources"),
        ("decision-nobreak.md", valid.replace("**Version:** 0.0.1\\", "**Version:** 0.0.1"), "missing trailing backslash"),
        ("decision-badclaimclass.md", valid.replace("**Claim Classes Present:** citation", "**Claim Classes Present:** citation, bogus"), "Claim Classes Present value"),
        ("decision-badlastreval.md", valid.replace("**Last Reviewed:** 2026-08-05", "**Last Reviewed:** 2026-13-99"), "not an ISO 8601"),
        ("decision-rootcorpusbody.md", valid.replace("Body cites [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md).", "Body cites [`specification-master-project.md`](../../specification-master-project.md)."), "not present in Corpus Sources"),
        ("decision-noneclaimclass.md", valid.replace("**Claim Classes Present:** citation", "**Claim Classes Present:** None"), "Claim Classes Present value"),
        ("decision-siblingreadme.md", valid.replace("Body cites [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md).", "Body cites [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md) and the entry point [README](README.md)."), None),
    ]
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        execroot = Path(td) / "executive"
        # Every case is a Decision Narrative, so it must live directly in executive/decision-narratives/.
        subdir = execroot / "decision-narratives"
        subdir.mkdir(parents=True)
        for name, content, expect in cases:
            p = subdir / name
            p.write_text(content, encoding="utf-8")
            findings = audit_page(p)
            if expect is None:
                if findings:
                    failures.append(f"{name}: expected PASS but got {findings}")
            else:
                if not any(expect in f for f in findings):
                    failures.append(f"{name}: expected a finding containing {expect!r}; got {findings}")
        # subtype -> subdirectory enforcement, two ways it can be wrong:
        # (a) right subtype dir name but wrong subtype: a Decision Narrative in briefs/.
        wrongdir = execroot / "briefs"
        wrongdir.mkdir()
        wp = wrongdir / "decision-wrongsubdir.md"
        wp.write_text(valid, encoding="utf-8")
        if not any("must live directly in executive/decision-narratives/" in f for f in audit_page(wp)):
            failures.append("decision-wrongsubdir.md: expected a subtype-subdir finding")
        # (b) correct subdir name but NOT a direct child of executive/ (nested).
        nesteddir = execroot / "archive" / "decision-narratives"
        nesteddir.mkdir(parents=True)
        npg = nesteddir / "decision-nested.md"
        npg.write_text(valid, encoding="utf-8")
        if not any("must live directly in executive/decision-narratives/" in f for f in audit_page(npg)):
            failures.append("decision-nested.md: expected a subtype-subdir finding for a nested page")
    if failures:
        for fl in failures:
            print(f"  SELF-TEST FAIL: {fl}")
        print(f"self-test: {len(failures)} case(s) failed out of {len(cases)}.")
        return 1
    print(f"self-test: {len(cases)} case(s) passed (valid page + {len(cases)-1} failure classes).")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv[1:]:
        return _self_test()
    args = [a for a in argv[1:] if not a.startswith("-")]
    if args:
        # 3b50: a missing path used to raise a FileNotFoundError traceback (rc 1); refuse it,
        # and an out-of-tree page (its pins resolve against THIS corpus), with exit 2.
        pages = [Path(a) for a in guard_explicit_paths_cwd(args)]
    else:
        pages = discover_pages()
    all_findings: list[str] = []
    for page in pages:
        all_findings.extend(audit_page(page))
    if all_findings:
        for f in all_findings:
            print(f"  {f}")
        print(f"FAIL: {len(all_findings)} narrative-metadata finding(s) across {len(pages)} page(s).")
        return 1
    print(f"OK: {len(pages)} narrative page(s) checked; all conform to the narrative metadata contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
