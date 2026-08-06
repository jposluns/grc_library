#!/usr/bin/env python3
"""Generate `narrative.yml` from the metadata of every executive narrative page.

Phase 1.2b of the executive narrative layer (the gate-family items 9/10
substrate). Authored from a verified worker draft.

`narrative.yml` is the generated, machine-readable registry of the narrative
layer: the analogue of `taxonomy.yml` for the root `executive/` tree
(specification-executive-narrative.md, "The narrative registry"). It is
regenerated from page metadata, never hand-edited, and carries per page: path,
title, narrative type, narrative status, version, date, corpus source pins
(as plain dependency paths, no versions), external sources, claim classes
present, review record identifier, last-reviewed date, and derived tags.
Derived classification lives ONLY here: never in page headers and never in
`taxonomy.yml`, which stays corpus-only by construction.

Discovery is ALWAYS the live `executive/` tree walk. The committed registry is
never a discovery source, in any mode: in `--check` it is only compared against
a fresh regeneration (string equality) and against a fresh, independent file
enumeration (the three-way bijection: executive/ files <-> registry rows <->
generated listing routes, with the named entry-point and redirect exclusions).

Corpus source pins are recorded as plain dependency PATHS. The narrative layer
has no dependency on corpus VERSIONS: an executive page refers to corpus
documents but never pins a version, so a corpus version bump never invalidates
a page. The only structural invalidation of a pin is a broken corpus link,
which the existing repository link and reference-integrity gates catch. The
generator never writes a pin and never edits a page.

Division of labour with the narrative metadata gate (gate 84,
tools/lint-narrative-metadata.py): gate 84 owns full metadata validation. This
generator fails LOUD (exit 2, writes nothing) only on what makes a row
unemittable: an unreadable page, a page with no metadata block, a missing
Document Title, or a Document Type other than `Executive Narrative`.

Usage:
    python3 tools/build-narrative-registry.py
    python3 tools/build-narrative-registry.py --check      # validate, no write
    python3 tools/build-narrative-registry.py --self-test  # synthetic pages

Exit codes: 0 in sync / written / self-test pass; 1 drift or bijection
failure; 2 unreadable or malformed candidate page (fail loud, nothing
written).

An `executive/` tree holding only the exempt entry-point README is valid:
the registry is generated empty (`pages: []`, `listing: []`) and `--check`
passes against that empty registry.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import METADATA_FIELD_RE, REPO_ROOT, read_text_safe

REGISTRY_NAME = "narrative.yml"
NARRATIVE_DOCUMENT_TYPE = "Executive Narrative"

# Named exclusions from the three-way bijection (spec Gates item 9). The entry
# point is the hand-curated concern-framing README: NOT a narrative page, NOT a
# registry row (spec "Placement and audit scope" item 4). Redirect stubs of
# superseded pages (spec "Release and retirement") follow the corpus
# EXEMPT_FROM_INDEX precedent (lint-structure.py / build-taxonomy.py): present
# for history, not active, named here explicitly. Empty today.
ENTRY_POINTS: frozenset[str] = frozenset({"executive/README.md"})
REDIRECT_EXCLUSIONS: frozenset[str] = frozenset()

# A Corpus Sources pin: a plain markdown link to the corpus document, no version
# suffix -- same grammar as gate 84 (tools/lint-narrative-metadata.py). Kept
# textually identical; hoisting the shared pin grammar into lint_common is a
# follow-up dedup for the integrator.
PIN_RE = re.compile(
    r"\[`(?P<disp>[^`]+)`\]\((?P<target>[^)]+)\)(?=[,\s]|$)"
)



# ---------------------------------------------------------------------------
# Small shared shapes (mirrors of gate 84 / build-taxonomy.py; dedup follow-up)

def yaml_escape(s: str) -> str:
    """Conservative YAML scalar escape: prefer double-quoted strings."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _yaml_unescape(s: str) -> str:
    return s.replace('\\"', '"').replace("\\\\", "\\")


def parse_metadata_block(text: str) -> dict[str, str]:
    """{field: value} for the leading metadata block (gate-84 semantics).

    The block ends at the first ``---`` separator or first blank line after at
    least one field. Strips the trailing backslash hard-break marker.
    """
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
            fields[name] = value
            seen = True
    return fields


def normalise_corpus_target(target: str) -> str:
    """Repo-relative corpus path of a pin target: strip leading ``./`` / ``../``
    segments and any anchor/query suffix (gate-84 semantics), so
    ``../risk/foo.md`` and ``risk/foo.md`` compare equal."""
    t = target.split("#", 1)[0].split("?", 1)[0]
    t = posixpath.normpath(t)
    while t.startswith("../") or t.startswith("./"):
        t = t[3:] if t.startswith("../") else t[2:]
    return t


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _parse_comma_list(value: str) -> list[str]:
    """Comma-separated field value -> list; ``None`` (the spec sentinel) -> []."""
    if not value or value.strip().lower() == "none":
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


# ---------------------------------------------------------------------------
# Input: the executive/ tree walk



def discover_pages(repo_root: Path) -> list[Path]:
    """Narrative pages: every .md under the root executive/ tree, minus the
    named entry-point and redirect exclusions. ALWAYS a live tree walk; the
    committed registry is never consulted for discovery. The walk is anchored
    at ``<repo_root>/executive`` by construction, so a nested directory merely
    named ``executive`` elsewhere is never reached (the is_narrative_root
    property, without binding to lint_common's module-level REPO_ROOT, so the
    self-test can run against a synthetic root)."""
    exec_root = repo_root / "executive"
    if not exec_root.is_dir():
        return []
    pages: list[Path] = []
    for p in sorted(exec_root.rglob("*.md")):
        rel = p.relative_to(repo_root).as_posix()
        if rel in ENTRY_POINTS or rel in REDIRECT_EXCLUSIONS:
            continue
        pages.append(p)
    return pages


# ---------------------------------------------------------------------------
# Row construction

def extract_pins(corpus_sources_value: str) -> list[str]:
    """The corpus dependency PATHS a page pins, in document order. Each is the
    normalized repo-relative corpus path of a well-formed pin (a plain markdown
    link, no version). A comma segment that is not a well-formed pin is surfaced
    verbatim (truncated) rather than silently dropped, so a malformed pin is
    loud in the registry; the metadata gate (gate 84) is the authority that
    blocks it. No version resolution: the registry has no dependency on corpus
    versions, so a corpus version bump never changes a page's registry row."""
    paths: list[str] = []
    for m in PIN_RE.finditer(corpus_sources_value):
        paths.append(normalise_corpus_target(m.group("target")))
    for seg in corpus_sources_value.split(","):
        seg = seg.strip()
        if not seg or seg.lower() == "none":
            continue
        if not PIN_RE.fullmatch(seg):
            paths.append(seg[:60])
    return paths


def derive_tags(ntype: str, nstatus: str, pins: list[str]) -> list[str]:
    """Mechanical derived tags: subtype, status, and domain coverage from the
    pin PATHS' top-level domain directories. Deliberately minimal: richer topic
    / audience-facet tagging is a policy decision deferred to the maintainer
    (see delivery notes); nothing here is guessed from prose."""
    tags: set[str] = set()
    if ntype:
        tags.add(f"type:{_slug(ntype)}")
    if nstatus:
        tags.add(f"status:{_slug(nstatus)}")
    for path in pins:
        head = path.split("/", 1)[0]
        if "/" in path and re.fullmatch(r"[a-z0-9-]+", head):
            tags.add(f"domain:{head}")
    return sorted(tags)


def build_rows(pages: list[Path], repo_root: Path) -> tuple[list[dict], list[str]]:
    """(registry rows sorted by path, hard errors). Any hard error means the
    tree holds an unemittable candidate page: fail loud, write nothing."""
    rows: list[dict] = []
    errors: list[str] = []
    for page in pages:
        rel = page.relative_to(repo_root).as_posix()
        text = read_text_safe(page)
        if text is None:
            errors.append(f"{rel}: not readable as UTF-8; cannot emit a registry row")
            continue
        meta = parse_metadata_block(text)
        if not meta:
            errors.append(f"{rel}: no metadata block found; cannot emit a registry row")
            continue
        doc_type = meta.get("Document Type", "")
        if doc_type != NARRATIVE_DOCUMENT_TYPE:
            errors.append(
                f"{rel}: Document Type must be {NARRATIVE_DOCUMENT_TYPE!r}, "
                f"got {doc_type!r}; not a well-formed narrative page "
                f"(see tools/lint-narrative-metadata.py)")
            continue
        title = meta.get("Document Title", "")
        if not title:
            errors.append(f"{rel}: missing Document Title; cannot emit a registry row")
            continue
        ntype = meta.get("Narrative Type", "")
        nstatus = meta.get("Narrative Status", "")
        pins = extract_pins(meta.get("Corpus Sources", ""))
        rows.append({
            "path": rel,
            "title": title,
            "narrative_type": ntype,
            "narrative_status": nstatus,
            "version": meta.get("Version", ""),
            "date": meta.get("Date", ""),
            "corpus_sources": pins,
            "external_sources": _parse_comma_list(meta.get("External Sources", "")),
            "claim_classes_present": _parse_comma_list(meta.get("Claim Classes Present", "")),
            "review_record": meta.get("Review Record", ""),
            "last_reviewed": meta.get("Last Reviewed", ""),
            "derived_tags": derive_tags(ntype, nstatus, pins),
        })
    rows.sort(key=lambda r: r["path"])
    return rows, errors


def route_for(rel_path: str) -> str:
    """The generated listing route for a page: its repo-relative path with the
    ``.md`` suffix dropped. Unique by construction (one file, one route)."""
    return rel_path[:-3] if rel_path.endswith(".md") else rel_path


# ---------------------------------------------------------------------------
# Emission (deterministic, hand-emitted YAML mirroring taxonomy.yml's style)

def _emit_str_list(key: str, values: list[str], indent: str = "  ") -> list[str]:
    if not values:
        return [f"{indent}{key}: []"]
    lines = [f"{indent}{key}:"]
    lines.extend(f"{indent}  - {yaml_escape(v)}" for v in values)
    return lines


def emit_row(row: dict) -> str:
    lines: list[str] = []
    lines.append(f"- path: {yaml_escape(row['path'])}")
    lines.append(f"  title: {yaml_escape(row['title'])}")
    lines.append(f"  narrative_type: {yaml_escape(row['narrative_type'])}")
    lines.append(f"  narrative_status: {yaml_escape(row['narrative_status'])}")
    lines.append(f"  version: {yaml_escape(row['version'])}")
    lines.append(f"  date: {yaml_escape(row['date'])}")
    lines.extend(_emit_str_list("corpus_sources", row["corpus_sources"]))
    lines.extend(_emit_str_list("external_sources", row["external_sources"]))
    lines.extend(_emit_str_list("claim_classes_present", row["claim_classes_present"]))
    lines.append(f"  review_record: {yaml_escape(row['review_record'])}")
    lines.append(f"  last_reviewed: {yaml_escape(row['last_reviewed'])}")
    lines.extend(_emit_str_list("derived_tags", row["derived_tags"]))
    return "\n".join(lines)


def build_registry_text(rows: list[dict]) -> str:
    """The full narrative.yml content: rows plus the generated listing.

    The listing section IS the generated artefact listing the narrative layer's
    orphan/listing gate (Gates item 10) keys off: every active page (every row;
    redirects are excluded upstream by name) appears as exactly one route.
    """
    out: list[str] = []
    out.append("# Auto-generated machine-readable narrative registry for the executive narrative layer.")
    out.append("# Source of truth: the metadata block of each narrative page under executive/.")
    out.append("# Corpus source pins are recorded as plain dependency paths (no versions).")
    out.append("# Regenerate with `python3 tools/build-narrative-registry.py`.")
    out.append("# Do not edit this file by hand. Derived classification lives ONLY here,")
    out.append("# never in page headers and never in taxonomy.yml (corpus-only by construction).")
    out.append("")
    out.append("schema_version: 1")
    out.append("generated_by: tools/build-narrative-registry.py")
    if rows:
        out.append("pages:")
        for r in rows:
            out.append(emit_row(r))
        out.append("listing:")
        for r in rows:  # rows are path-sorted; routes inherit that order
            out.append(f"- route: {yaml_escape(route_for(r['path']))}")
            out.append(f"  path: {yaml_escape(r['path'])}")
            out.append(f"  title: {yaml_escape(r['title'])}")
    else:
        out.append("pages: []")
        out.append("listing: []")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# The three-way bijection: executive/ files <-> registry rows <-> listing routes

def bijection_findings(page_rels: list[str], row_paths: list[str],
                       routes: list[str]) -> list[str]:
    """Findings when the three independently supplied enumerations do not
    biject. ``page_rels`` must come from a FRESH tree walk, never from the
    registry under test."""
    findings: list[str] = []
    files, rows_set, routes_set = set(page_rels), set(row_paths), set(routes)
    dup_rows = {p for p in row_paths if row_paths.count(p) > 1}
    dup_routes = {r for r in routes if routes.count(r) > 1}
    for p in sorted(dup_rows):
        findings.append(f"duplicate registry row for page: {p}")
    for r in sorted(dup_routes):
        findings.append(f"duplicate listing route: {r}")
    for p in sorted(files - rows_set):
        findings.append(f"executive/ page has no registry row (orphan): {p}")
    for p in sorted(rows_set - files):
        findings.append(f"registry row has no executive/ file: {p}")
    expected_routes = {route_for(p) for p in rows_set}
    for r in sorted(expected_routes - routes_set):
        findings.append(f"registry row has no generated listing route (orphan from listing): {r}")
    for r in sorted(routes_set - expected_routes):
        findings.append(f"generated listing route has no registry row: {r}")
    return findings


_COMMITTED_ROW_RE = re.compile(r'^- path: "(?P<v>(?:[^"\\]|\\.)*)"\s*$')
_COMMITTED_ROUTE_RE = re.compile(r'^- route: "(?P<v>(?:[^"\\]|\\.)*)"\s*$')


def parse_committed_registry(text: str) -> tuple[list[str], list[str]]:
    """(row paths, listing routes) from a committed narrative.yml. Used ONLY
    to compare the committed registry against the live tree; never to
    discover pages."""
    row_paths: list[str] = []
    routes: list[str] = []
    section = ""
    for line in text.splitlines():
        if line.startswith("pages:"):
            section = "pages"
            continue
        if line.startswith("listing:"):
            section = "listing"
            continue
        if section == "pages":
            m = _COMMITTED_ROW_RE.match(line)
            if m:
                row_paths.append(_yaml_unescape(m.group("v")))
        elif section == "listing":
            m = _COMMITTED_ROUTE_RE.match(line)
            if m:
                routes.append(_yaml_unescape(m.group("v")))
    return row_paths, routes


# ---------------------------------------------------------------------------
# Modes

def run(repo_root: Path, check: bool) -> int:
    registry_path = repo_root / REGISTRY_NAME

    pages = discover_pages(repo_root)
    rows, errors = build_rows(pages, repo_root)
    if errors:
        for e in errors:
            print(f"  {e}")
        print(f"FAIL: {len(errors)} unreadable/malformed candidate page(s); "
              f"nothing {'checked' if check else 'written'}. Fix the page(s) "
              f"(tools/lint-narrative-metadata.py reports the full metadata contract).")
        return 2

    new_content = build_registry_text(rows)
    page_rels = [p.relative_to(repo_root).as_posix() for p in pages]

    # Internal three-way bijection on the fresh build (defence in depth: this
    # can only fail if the generator itself is broken).
    internal = bijection_findings(page_rels,
                                  [r["path"] for r in rows],
                                  [route_for(r["path"]) for r in rows])
    if internal:
        for f in internal:
            print(f"  {f}")
        print(f"FAIL: {len(internal)} internal bijection finding(s) in the fresh build.")
        return 1

    if check:
        if not registry_path.exists():
            print(f"FAIL: {REGISTRY_NAME} does not exist; run without --check to generate.")
            return 1
        current = read_text_safe(registry_path)
        if current is None:
            print(f"FAIL: {REGISTRY_NAME} is not readable as UTF-8.")
            return 1
        findings: list[str] = []
        # Three-way bijection of the COMMITTED registry against a fresh,
        # independent tree walk (never discovery -- comparison only).
        committed_rows, committed_routes = parse_committed_registry(current)
        findings.extend(bijection_findings(page_rels, committed_rows, committed_routes))
        if current != new_content:
            findings.append(f"{REGISTRY_NAME} content differs from a fresh regeneration "
                            f"(metadata, pin, or listing drift)")
        if findings:
            for f in findings:
                print(f"  {f}")
            print(f"FAIL: {REGISTRY_NAME} is out of sync with the executive/ tree.")
            print("Run `python3 tools/build-narrative-registry.py` to regenerate.")
            return 1
        print(f"OK: {REGISTRY_NAME} is in sync ({len(rows)} page(s); "
              f"files <-> rows <-> routes biject).")
        return 0

    registry_path.write_text(new_content, encoding="utf-8")
    print(f"Wrote {REGISTRY_NAME} ({len(new_content.splitlines())} lines, {len(rows)} page(s)).")
    return 0


# ---------------------------------------------------------------------------
# Self-test: synthetic pages against a synthetic repo root

_ST_PAGE_TEMPLATE = """# {title}

**Document Title:** {title}\\
**Document Type:** Executive Narrative\\
**Version:** 0.0.1\\
**Date:** 2026-08-05\\
**Owner:** Governance Library Maintainer\\
**Approving Authority:** Governance Library Maintainer\\
**Related Documents:** [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)\\
**Classification:** Public\\
**Category:** Executive Narrative\\
**Review Frequency:** Annual\\
**Repository Path:** [`executive/{name}`]({name})\\
**Confidentiality:** Public\\
**License:** CC BY-SA 4.0\\
**Narrative Type:** Decision Narrative\\
**Narrative Status:** Advisory\\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\\
**Corpus Sources:** {pins}\\
**External Sources:** {external}\\
**Claim Classes Present:** citation\\
**Review Record:** NR-2026-001\\
**Last Reviewed:** 2026-08-05

---

Body.
"""

def _st_make_root(td: Path, pages: dict[str, str]) -> Path:
    root = td
    (root / "executive").mkdir(parents=True, exist_ok=True)
    (root / "executive" / "README.md").write_text("# Executive narratives\n", encoding="utf-8")
    for name, content in pages.items():
        (root / "executive" / name).write_text(content, encoding="utf-8")
    return root


def _st_page(name: str, pins: str, external: str = "None") -> str:
    title = name[:-3].replace("-", " ").title()
    return _ST_PAGE_TEMPLATE.format(title=title, name=name, pins=pins, external=external)


_PIN_OK = "[`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)"
_PIN_GOV = "[`governance/charter-governance-library.md`](../governance/charter-governance-library.md)"
# A leftover @version suffix is no longer a well-formed pin: it is surfaced verbatim.
_PIN_MALFORMED = "[`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)@1.0.6"


def _self_test() -> int:
    """Prove pin-path extraction, derived tags, deterministic emission, the
    fail-loud path, the empty-tree case, the bijection detector, and check-mode
    drift against synthetic pages (the live executive/ tree holds only the
    exempt README today, zero real pages). Mirrors gates 82/84's discipline."""
    import tempfile

    failures: list[str] = []

    def expect(cond: bool, label: str) -> None:
        if not cond:
            failures.append(label)

    with tempfile.TemporaryDirectory() as td_s:
        # Case set 1: pins-as-paths + rows + listing on a populated tree.
        root = _st_make_root(Path(td_s) / "r1", {
            "decision-two.md": _st_page("decision-two.md", f"{_PIN_OK}, {_PIN_GOV}", external="ISO 31000"),
            "decision-one.md": _st_page("decision-one.md", _PIN_OK),
            "decision-dup.md": _st_page("decision-dup.md", f"{_PIN_OK}, [`risk/annex-ai-risk-methodology.md`](risk/annex-ai-risk-methodology.md)"),
            "decision-malformed.md": _st_page("decision-malformed.md", f"{_PIN_OK}, {_PIN_MALFORMED}"),
            "decision-nopin.md": _st_page("decision-nopin.md", "None"),
        })
        pages = discover_pages(root)
        expect(len(pages) == 5, f"discovery: expected 5 pages (README exempt), got {len(pages)}")
        rows, errors = build_rows(pages, root)
        expect(not errors, f"populated tree: unexpected hard errors {errors}")
        by = {r["path"].rsplit("/", 1)[-1]: r for r in rows}
        expect(by["decision-two.md"]["corpus_sources"] ==
               ["risk/annex-ai-risk-methodology.md", "governance/charter-governance-library.md"],
               f"two-pin paths: {by['decision-two.md']['corpus_sources']}")
        expect(by["decision-nopin.md"]["corpus_sources"] == [],
               f"no-pin paths: {by['decision-nopin.md']['corpus_sources']}")
        expect(by["decision-dup.md"]["corpus_sources"] ==
               ["risk/annex-ai-risk-methodology.md", "risk/annex-ai-risk-methodology.md"],
               f"dup paths surfaced twice: {by['decision-dup.md']['corpus_sources']}")
        expect(any(pp.startswith("[") for pp in by["decision-malformed.md"]["corpus_sources"]),
               f"malformed pin surfaced verbatim: {by['decision-malformed.md']['corpus_sources']}")
        expect("staleness_state" not in by["decision-two.md"], "no staleness_state field on a row")
        expect(by["decision-two.md"]["derived_tags"] == ["domain:governance", "domain:risk",
                                       "status:advisory", "type:decision-narrative"],
               f"derived tags: {by['decision-two.md']['derived_tags']}")
        expect(by["decision-two.md"]["external_sources"] == ["ISO 31000"],
               f"external sources: {by['decision-two.md']['external_sources']}")
        expect(rows == sorted(rows, key=lambda r: r["path"]), "rows not path-sorted")
        text1 = build_registry_text(rows)
        expect("staleness" not in text1, "generated registry must not mention staleness")
        expect(build_registry_text(rows) == text1, "emission not deterministic")
        committed_rows, committed_routes = parse_committed_registry(text1)
        expect(len(committed_rows) == 5 and len(committed_routes) == 5,
               f"committed-registry parse: {len(committed_rows)} rows, {len(committed_routes)} routes")
        page_rels = [pg.relative_to(root).as_posix() for pg in pages]
        expect(bijection_findings(page_rels, committed_rows, committed_routes) == [],
               "fresh build should biject")
        # Bijection detector: extra row, missing route, orphan file.
        expect(any("no executive/ file" in f for f in
                   bijection_findings(page_rels, committed_rows + ["executive/decision-ghost.md"],
                                      committed_routes + ["executive/decision-ghost"])),
               "extra committed row not detected")
        expect(any("orphan from listing" in f for f in
                   bijection_findings(page_rels, committed_rows, committed_routes[:-1])),
               "missing listing route (orphan) not detected")
        expect(any("orphan" in f for f in
                   bijection_findings(page_rels + ["executive/decision-new.md"],
                                      committed_rows, committed_routes)),
               "file without registry row (orphan) not detected")
        # End-to-end: write, check OK, then edit a page and expect check FAIL.
        expect(run(root, check=False) == 0, "write mode should succeed on populated tree")
        expect(run(root, check=True) == 0, "check should pass right after generation")
        edited = root / "executive" / "decision-one.md"
        edited.write_text(edited.read_text(encoding="utf-8").replace("**Version:** 0.0.1", "**Version:** 0.0.2"), encoding="utf-8")
        expect(run(root, check=True) == 1, "check should fail (exit 1) after a page edit")

        # Case set 2: fail-loud on a malformed candidate page.
        root2 = _st_make_root(Path(td_s) / "r2", {
            "decision-ok.md": _st_page("decision-ok.md", _PIN_OK),
            "decision-notnarrative.md": _st_page("decision-notnarrative.md", _PIN_OK).replace(
                "**Document Type:** Executive Narrative", "**Document Type:** Guide"),
        })
        expect(run(root2, check=False) == 2, "malformed page: build must fail loud (exit 2), write nothing")
        expect(not (root2 / REGISTRY_NAME).exists(), "malformed page: registry must not be written")
        expect(run(root2, check=True) == 2, "malformed page: check must fail loud (exit 2)")

        # Case set 3: the empty tree (only the exempt README) generates an
        # empty registry and check passes against it.
        root3 = _st_make_root(Path(td_s) / "r3", {})
        expect(discover_pages(root3) == [], "empty tree: no pages discovered")
        expect(run(root3, check=False) == 0, "empty tree: generation must pass")
        empty_text = (root3 / REGISTRY_NAME).read_text(encoding="utf-8")
        expect("pages: []" in empty_text and "listing: []" in empty_text,
               "empty tree: registry must carry pages: [] and listing: []")
        expect("staleness" not in empty_text, "empty registry header must not mention staleness")
        expect(run(root3, check=True) == 0, "empty tree: check must pass")
        # A page added after generation drifts the committed empty registry.
        (root3 / "executive" / "decision-late.md").write_text(
            _st_page("decision-late.md", _PIN_OK), encoding="utf-8")
        expect(run(root3, check=True) == 1, "page added after generation: check must fail")

    if failures:
        for f in failures:
            print(f"  SELF-TEST FAIL: {f}")
        print(f"self-test: {len(failures)} assertion(s) failed.")
        return 1
    print("self-test: all assertions passed (pin-path extraction, fail-loud, empty "
          "tree, bijection detector, check-mode drift).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate narrative.yml (the executive narrative registry) from page metadata.")
    parser.add_argument("--check", action="store_true",
                        help="Validate that narrative.yml is in sync with the executive/ tree "
                             "(fresh regeneration + three-way bijection); do not write. "
                             "Exits 1 on drift, 2 on a malformed candidate page.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run the synthetic-page self-test and exit.")
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    return run(REPO_ROOT, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
