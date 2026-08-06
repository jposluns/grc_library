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

import posixpath
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import METADATA_FIELD_RE, REPO_ROOT, is_narrative_root, parse_iso_date, read_text_safe

NARRATIVE_DOCUMENT_TYPE = "Executive Narrative"
ENTRY_POINT = "executive/README.md"  # the single named non-narrative-page exemption

# The 13 canonical fields, in canonical order (mirrors the corpus model).
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

# The 8 narrative-extension fields, in order, appended after License.
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

# The seven closed subtypes: Narrative Type -> (filename prefix, fixed Narrative
# Status, subtype subdirectory under ``executive/``). Each subtype lives in its own
# subdirectory so the layer stays organized as content grows.
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

# A Corpus Sources pin: a plain markdown link to the corpus document, NO version
# suffix, e.g.
# [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)
PIN_RE = re.compile(r"\[`(?P<disp>[^`]+)`\]\((?P<target>[^)]+)\)(?=[,\s]|$)")
# A markdown link in the page body (for body-link/pin completeness).
BODY_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)]+)\)")
# Corpus domain dirs a body link would point into (a link is "to the corpus" if
# its resolved target lands in one of these top-level dirs).
CORPUS_DOMAIN_PREFIXES = (
    "ai/", "architecture/", "compliance/", "dev-security/", "governance/",
    "operations/", "privacy/", "resilience/", "risk/", "security/", "supply-chain/",
)
# Root-level corpus documents (the corpus metadata gate's by-name root scan set,
# mirrored here so a body link to a ROOT corpus doc is covered by pin-completeness too;
# keep in sync with the by-name list in tools/lint-metadata.py main()).
ROOT_CORPUS_DOCS = frozenset({
    "README.md", "NOTICE.md", "specification-master-project.md",
    "specification-ingestion.md", "specification-executive-narrative.md",
    "instruction-ai-document-ingestion.md",
})
# The closed Claim Classes Present vocabulary (spec claim-classes section).
CLAIM_CLASSES = frozenset({"citation", "sourced", "composite"})


def parse_metadata_block(text: str) -> tuple[list[str], dict[str, str]]:
    """Return (ordered field names, {field: value}) for the leading metadata block.

    The block ends at the first ``---`` separator or first blank line after at
    least one field. Strips the trailing backslash hard-break marker from values.
    """
    order: list[str] = []
    fields: dict[str, str] = {}
    seen = False
    for line in text.splitlines():
        stripped = line.strip()
        if seen and (stripped.startswith("---") or not stripped):
            break
        m = METADATA_FIELD_RE.match(line)
        if m:
            name, value = m.group(1).strip(), m.group(2).strip()
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            order.append(name)
            fields[name] = value
            seen = True
    return order, fields


def _metadata_run_lines(text: str) -> list[str]:
    """The raw lines of the leading metadata block (for hard-break checking)."""
    run: list[str] = []
    seen = False
    for line in text.splitlines():
        stripped = line.strip()
        if seen and (stripped.startswith("---") or not stripped):
            break
        if METADATA_FIELD_RE.match(line):
            run.append(line)
            seen = True
        elif seen:
            run.append(line)
    return run


def check_hard_breaks(text: str) -> list[str]:
    """Every metadata-run line except the last must end with a backslash marker."""
    run = _metadata_run_lines(text)
    findings: list[str] = []
    for line in run[:-1]:
        if not line.rstrip().endswith("\\"):
            findings.append(f"metadata line missing trailing backslash hard-break: {line.strip()[:60]!r}")
    if run and run[-1].rstrip().endswith("\\"):
        findings.append(f"the block's last metadata line must be bare (no trailing backslash): {run[-1].strip()[:60]!r}")
    return findings


def _normalise_corpus_target(target: str) -> str:
    """Reduce a pin or body-link target to its repo-relative corpus path by
    stripping leading ``./`` and ``../`` segments, so ``../risk/foo.md`` and
    ``risk/foo.md`` compare equal while a same-basename file in a different
    domain (``governance/foo.md``) does NOT. Any anchor/query suffix is dropped."""
    t = target.split("#", 1)[0].split("?", 1)[0]
    # Collapse INTERNAL traversal first (posixpath.normpath is pure, no filesystem),
    # so `../risk/../executive/x.md` resolves to `executive/x.md` and cannot pose as a
    # `risk/` corpus doc; then strip the leading up-segments out of executive/.
    t = posixpath.normpath(t)
    while t.startswith("../") or t.startswith("./"):
        t = t[3:] if t.startswith("../") else t[2:]
    return t


def audit_page(path: Path) -> list[str]:
    try:
        rel = path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        rel = path.as_posix()
    text = read_text_safe(path)
    if text is None:
        return [f"{rel}: not readable / not utf-8"]
    findings: list[str] = []
    order, meta = parse_metadata_block(text)

    # Document Type
    if meta.get("Document Type") != NARRATIVE_DOCUMENT_TYPE:
        findings.append(f"{rel}: Document Type must be {NARRATIVE_DOCUMENT_TYPE!r}, got {meta.get('Document Type')!r}")

    # Canonical 13 present + in canonical order (as a prefix of the block order).
    for fld in CANONICAL_FIELDS:
        if fld not in meta:
            findings.append(f"{rel}: missing canonical field: {fld}")
    # Extension 8 present.
    for fld in EXTENSION_FIELDS:
        if fld not in meta:
            findings.append(f"{rel}: missing narrative-extension field: {fld}")
    # Order: the block order must equal canonical-13 then extension-8 (for the fields present).
    known = set(CANONICAL_FIELDS + EXTENSION_FIELDS)
    unknown = [fld for fld in order if fld not in known]
    if unknown:
        findings.append(f"{rel}: unexpected metadata field(s) (the 8-field extension must follow the 13 canonical fields immediately, no interposed fields): {unknown}")
    expected_order = [f for f in CANONICAL_FIELDS + EXTENSION_FIELDS if f in meta]
    present_in_block = [f for f in order if f in known]
    if present_in_block != expected_order:
        findings.append(f"{rel}: metadata fields out of canonical order (expected 13 canonical then 8 extension)")

    # Narrative Type / Status / prefix / status-parity.
    ntype = meta.get("Narrative Type")
    nstatus = meta.get("Narrative Status")
    if ntype is not None and ntype not in SUBTYPES:
        findings.append(f"{rel}: Narrative Type {ntype!r} not one of the seven closed subtypes")
    if nstatus is not None and nstatus not in STATUSES:
        findings.append(f"{rel}: Narrative Status {nstatus!r} not one of {sorted(STATUSES)}")
    if ntype in SUBTYPES:
        prefix, fixed_status, subdir = SUBTYPES[ntype]
        if nstatus is not None and nstatus != fixed_status:
            findings.append(f"{rel}: Narrative Status {nstatus!r} does not match the fixed status {fixed_status!r} for {ntype!r}")
        if not path.name.startswith(prefix):
            findings.append(f"{rel}: filename must start with {prefix!r} for Narrative Type {ntype!r}")
        if path.parent.name != subdir or path.parent.parent.name != "executive":
            findings.append(f"{rel}: a {ntype!r} page must live directly in executive/{subdir}/")

    # Corpus Sources pins.
    corpus_sources = meta.get("Corpus Sources", "")
    pins = PIN_RE.findall(corpus_sources)
    pin_targets = [m[1] for m in pins]
    if not pins:
        findings.append(f"{rel}: Corpus Sources must carry at least one pin of the form [`path`](path)")
    # Malformed pin: a comma-separated segment that is not a bare markdown link
    # (e.g. a leftover `@version` suffix, or free text). A segment that is just
    # `none` is skipped (a bare `None`).
    for seg in corpus_sources.split(","):
        seg = seg.strip()
        if not seg or seg.lower() == "none":
            continue
        # The WHOLE segment must be exactly one bare markdown link (fullmatch), so a
        # malformed pin cannot hide after a valid one in the same space-separated segment.
        if not PIN_RE.fullmatch(seg):
            findings.append(f"{rel}: malformed Corpus Sources pin (each entry must be exactly a bare markdown link [`path`](path), comma-separated): {seg[:80]!r}")
    # Duplicate check on the NORMALISED corpus path, so `../risk/x.md` and `risk/x.md` count as one target.
    norm_targets = [_normalise_corpus_target(t) for t in pin_targets]
    dupes = {t for t in norm_targets if norm_targets.count(t) > 1}
    for t in sorted(dupes):
        findings.append(f"{rel}: duplicate Corpus Sources pin on the same target: {t}")
    # Corpus-membership: each pin must reference a corpus DOCUMENT, which lives
    # OUTSIDE executive/. A corpus pin therefore traverses up ("../") and lands
    # under a corpus domain dir or is a root corpus doc. A bare or non-traversing
    # target points inside executive/ (a sibling page, e.g. the entry-point
    # README) or out of the corpus, and is not a corpus source. (The redesign
    # dropped gate 85's taxonomy-based membership test; gate 84 is now the
    # authority that a pin names a corpus document. Mirrors the body-link rule.)
    for t in pin_targets:
        norm = _normalise_corpus_target(t)
        goes_up = t.strip().startswith(("../", "..\\"))
        # A CLEAN corpus path only: reject any residual traversal or an encoding
        # (`%..`, `\\`) that a renderer might later decode into traversal, so an
        # obfuscated non-corpus target cannot pose as a corpus doc after normpath.
        clean = bool(norm) and ".." not in norm.split("/") and "%" not in norm and "\\" not in norm
        is_corpus = goes_up and clean and (any(norm.startswith(pre) for pre in CORPUS_DOMAIN_PREFIXES) or norm in ROOT_CORPUS_DOCS)
        if not is_corpus:
            findings.append(f"{rel}: Corpus Sources pin target {t!r} is not a corpus document (a pin must reference a corpus document outside executive/)")

    # Closed-vocabulary / typed value validation for extension fields (defence-in-depth
    # beyond the presence checks above; the constraints are stated in the spec's metadata
    # and claim-classes sections though Gates item 4 enumerates only Narrative Type/Status).
    claim_classes = meta.get("Claim Classes Present")
    if claim_classes is not None:
        for tok in (t.strip() for t in claim_classes.split(",")):
            if tok and tok not in CLAIM_CLASSES:
                findings.append(f"{rel}: Claim Classes Present value {tok!r} not one of {sorted(CLAIM_CLASSES)}")
    last_reviewed = meta.get("Last Reviewed")
    if last_reviewed is not None and parse_iso_date(last_reviewed) is None:
        findings.append(f"{rel}: Last Reviewed {last_reviewed!r} is not an ISO 8601 (YYYY-MM-DD) date")

    # Body-link/pin completeness: a body corpus link absent from Corpus Sources is a defect.
    # Match on the FULL repo-relative corpus path (not the basename): a same-named
    # file in another domain must not count as pinned.
    hdr_anchor = text.find(EXTENSION_FIELDS[-1])
    body_start = text.find("\n---", hdr_anchor) if hdr_anchor != -1 else -1
    body = text[body_start:] if body_start > 0 else text
    pinned_norm = {_normalise_corpus_target(t) for t in pin_targets}
    for m in BODY_LINK_RE.finditer(body):
        target = m.group("target")
        norm = _normalise_corpus_target(target)
        # A corpus document is OUTSIDE executive/, so a corpus body link must traverse up ("../");
        # a bare basename is a sibling inside executive/ (e.g. the entry-point README), not corpus.
        goes_up = target.strip().startswith(("../", "..\\"))
        if goes_up and (any(norm.startswith(p) for p in CORPUS_DOMAIN_PREFIXES) or norm in ROOT_CORPUS_DOCS):
            if norm not in pinned_norm:
                findings.append(f"{rel}: body links corpus document {target!r} not present in Corpus Sources pins")

    # Hard breaks.
    findings.extend(f"{rel}: {f}" for f in check_hard_breaks(text))
    return findings


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
        pages = [Path(a).resolve() for a in args]
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
