#!/usr/bin/env python3
"""Executive-narrative metadata contract - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A; narrative-family, the last
narrative gate): the PURE metadata-contract scan (parse_metadata_block, _metadata_run_lines,
check_hard_breaks, _normalise_corpus_target, audit_page) is the source of record here in the
pack, moved verbatim from the grc gate. The project-content sets (narrative document type,
entry-point exemption, canonical + extension field orders, the subtype table, the status and
claim-class vocabularies, the corpus domain prefixes + root corpus docs, and the repository
root) are supplied by the adopter via configure(ref), so the engine is project-agnostic (its
finding-message text carries the configured names literally, a byte-identity residue of the
verbatim transfer). The markdown pin/body-link structural regexes are engine-fixed. The grc
wrapper (tools/lint-narrative-metadata.py) supplies the content sets + the page scan scope
(discover_pages), configures the engine, and keeps the self-test, main, and the module-global
audit_page shim.
"""

from __future__ import annotations

import posixpath
import re

try:
    from aiqt_corpus import METADATA_FIELD_RE, parse_iso_date, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_narrative_metadata: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Project-content sets + repo root: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
NARRATIVE_DOCUMENT_TYPE = ""
ENTRY_POINT = ""
CANONICAL_FIELDS: list = []
EXTENSION_FIELDS: list = []
SUBTYPES: dict = {}
STATUSES = frozenset()
CORPUS_DOMAIN_PREFIXES: tuple = ()
ROOT_CORPUS_DOCS = frozenset()
CLAIM_CLASSES = frozenset()
REPO_ROOT = None


def configure(ref) -> None:
    """Populate the project-content sets + repo root from the adopter. The scan functions
    resolve these as module globals; call once before audit_page()."""
    global NARRATIVE_DOCUMENT_TYPE, ENTRY_POINT, CANONICAL_FIELDS, EXTENSION_FIELDS, SUBTYPES
    global STATUSES, CORPUS_DOMAIN_PREFIXES, ROOT_CORPUS_DOCS, CLAIM_CLASSES, REPO_ROOT
    NARRATIVE_DOCUMENT_TYPE = ref.narrative_document_type
    ENTRY_POINT = ref.entry_point
    CANONICAL_FIELDS = ref.canonical_fields
    EXTENSION_FIELDS = ref.extension_fields
    SUBTYPES = ref.subtypes
    STATUSES = ref.statuses
    CORPUS_DOMAIN_PREFIXES = ref.corpus_domain_prefixes
    ROOT_CORPUS_DOCS = ref.root_corpus_docs
    CLAIM_CLASSES = ref.claim_classes
    REPO_ROOT = ref.repo_root


# Structural markdown regexes (pin and body-link shapes): engine-fixed, project-agnostic.
PIN_RE = re.compile(r"\[`(?P<disp>[^`]+)`\]\((?P<target>[^)]+)\)(?=[,\s]|$)")
BODY_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)]+)\)")


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
