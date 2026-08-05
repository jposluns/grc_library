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
  - At least one ``Corpus Sources`` pin, each of the form ``path@semver`` with a
    single pin per target (no duplicate pin on the same target).
  - Body-link/pin completeness: every corpus document linked in the page body
    appears in ``Corpus Sources``.
  - Backslash hard-break markers on every metadata line except the block's last.

Exit 0 if every narrative page is valid (an executive/ tree holding only the
entry-point README is valid: zero pages, zero findings). Exit 1 on any finding.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import METADATA_FIELD_RE, REPO_ROOT, is_narrative_root, read_text_safe

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
    "Last Revalidated",
]

# The seven closed subtypes: Narrative Type -> (filename prefix, fixed Narrative Status).
SUBTYPES: dict[str, tuple[str, str]] = {
    "Executive Brief": ("brief-", "Explanatory"),
    "Scenario": ("scenario-", "Non-normative"),
    "Decision Narrative": ("decision-", "Advisory"),
    "Oversight Question Set": ("oversight-questions-", "Advisory"),
    "Story": ("story-", "Non-normative"),
    "Journey": ("journey-", "Explanatory"),
    "Outcome Map": ("outcome-map-", "Explanatory"),
}
STATUSES: frozenset[str] = frozenset({"Non-normative", "Advisory", "Explanatory"})

# A Corpus Sources pin: a markdown link followed by @semver, e.g.
# [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6
PIN_RE = re.compile(r"\[`(?P<disp>[^`]+)`\]\((?P<target>[^)]+)\)@(?P<ver>\d+\.\d+\.\d+)(?=[,\s]|$)")
# A markdown link in the page body (for body-link/pin completeness).
BODY_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)]+)\)")
# Corpus domain dirs a body link would point into (a link is "to the corpus" if
# its resolved target lands in one of these top-level dirs).
CORPUS_DOMAIN_PREFIXES = (
    "ai/", "architecture/", "compliance/", "dev-security/", "governance/",
    "operations/", "privacy/", "resilience/", "risk/", "security/", "supply-chain/",
)


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
        prefix, fixed_status = SUBTYPES[ntype]
        if nstatus is not None and nstatus != fixed_status:
            findings.append(f"{rel}: Narrative Status {nstatus!r} does not match the fixed status {fixed_status!r} for {ntype!r}")
        if not path.name.startswith(prefix):
            findings.append(f"{rel}: filename must start with {prefix!r} for Narrative Type {ntype!r}")

    # Corpus Sources pins.
    corpus_sources = meta.get("Corpus Sources", "")
    pins = PIN_RE.findall(corpus_sources)
    pin_targets = [m[1] for m in pins]
    if not pins:
        findings.append(f"{rel}: Corpus Sources must carry at least one pin of the form [`path`](path)@semver")
    # Malformed pin: a comma-separated segment carrying an @-version that is not a well-formed pin
    # (e.g. `@1.0.6junk`, a trailing garbage version). Segments with no `@` are skipped (a bare `None`).
    for seg in corpus_sources.split(","):
        seg = seg.strip()
        if not seg or seg.lower() == "none":
            continue
        # The WHOLE segment must be exactly one pin (fullmatch), so a malformed pin
        # cannot hide after a valid one in the same space-separated segment.
        if not PIN_RE.fullmatch(seg):
            findings.append(f"{rel}: malformed Corpus Sources pin (each entry must be exactly [`path`](path)@semver, comma-separated): {seg[:80]!r}")
    # Duplicate check on the NORMALISED corpus path, so `../risk/x.md` and `risk/x.md` count as one target.
    norm_targets = [_normalise_corpus_target(t) for t in pin_targets]
    dupes = {t for t in norm_targets if norm_targets.count(t) > 1}
    for t in sorted(dupes):
        findings.append(f"{rel}: duplicate Corpus Sources pin on the same target: {t}")

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
        if any(norm.startswith(p) for p in CORPUS_DOMAIN_PREFIXES):
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
**Related Documents:** [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)\\
**Classification:** Public\\
**Category:** Executive Narrative\\
**Review Frequency:** Annual\\
**Repository Path:** [`executive/decision-ai-risk-appetite.md`](decision-ai-risk-appetite.md)\\
**Confidentiality:** Public\\
**License:** CC BY-SA 4.0\\
**Narrative Type:** Decision Narrative\\
**Narrative Status:** Advisory\\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\\
**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6\\
**External Sources:** None\\
**Claim Classes Present:** citation\\
**Review Record:** NR-2026-001\\
**Last Revalidated:** 2026-08-05

---

Body cites [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md).
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
        ("decision-malformedpin.md", valid.replace("@1.0.6\\", "@1.0.6junk\\"), "malformed Corpus Sources pin"),
        ("decision-hiddenmalformed.md", valid.replace("[`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6\\", "[`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6 [`governance/charter-governance-library.md`](../governance/charter-governance-library.md)@2.0.0junk\\"), "malformed Corpus Sources pin"),
        ("decision-aliasdup.md", valid.replace("**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6", "**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6, [`risk/annex-ai-risk-methodology.md`](risk/annex-ai-risk-methodology.md)@1.0.6"), "duplicate Corpus Sources pin"),
        ("decision-lastbackslash.md", valid.replace("**Last Revalidated:** 2026-08-05", "**Last Revalidated:** 2026-08-05\\"), "last metadata line must be bare"),
        ("decision-interposed.md", valid.replace("**License:** CC BY-SA 4.0\\", "**License:** CC BY-SA 4.0\\\n**Bogus Field:** x\\"), "unexpected metadata field"),
        ("wrongprefix.md", valid, "filename must start with"),
        ("decision-nopin.md", re.sub(r"\*\*Corpus Sources:\*\*.*", "**Corpus Sources:** none\\\\", valid), "at least one pin"),
        ("decision-duppin.md", valid.replace("**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6", "**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6, [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6"), "duplicate Corpus Sources pin"),
        ("decision-unpinnedbody.md", valid.replace("Body cites [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md).", "Body links [`governance/charter-governance-library.md`](../governance/charter-governance-library.md)."), "not present in Corpus Sources"),
        ("decision-nobreak.md", valid.replace("**Version:** 0.0.1\\", "**Version:** 0.0.1"), "missing trailing backslash"),
    ]
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        for name, content, expect in cases:
            p = Path(td) / name
            p.write_text(content, encoding="utf-8")
            findings = audit_page(p)
            if expect is None:
                if findings:
                    failures.append(f"{name}: expected PASS but got {findings}")
            else:
                if not any(expect in f for f in findings):
                    failures.append(f"{name}: expected a finding containing {expect!r}; got {findings}")
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
